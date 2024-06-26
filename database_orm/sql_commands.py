from .column import Column


class CreateTable:

    def __init__(self, table):

        compiled_columns = str()
        for name, value in table.__dict__.items():

            if not name.startswith("__"):
                setattr(value, "__namecolumn__", name)
                compiled_columns += f"{name} {value.__sqloperation__}, "
        self.sql = f"CREATE TABLE IF NOT EXISTS {table.__name__}s({compiled_columns[:-2]});"
        self.table = table
        self.args = ()


class NewRow:
    from .data_types import Serial
    __sqlopeartion__: str

    def __init__(self, table, **kwargs):
        sort_names = str()
        sort_vars = str()
        args = []
        i = 1
        for name, value in table.__dict__.items():
            if not name.startswith("__"):
                val = kwargs.get(name)
                pass_value = False
                if val is None:
                    if self.Serial != type(value.data_type) and value.not_null:
                        error = f"{table.__name__} missing 1 required positional argument: '{name}'"
                        raise TypeError(error)
                    else:
                        pass_value = True
                else:
                    if self.Serial == type(value.data_type):
                        raise TypeError("SERIAL type do not take value")
                if not pass_value:
                    sort_names += f"{name},"
                    sort_vars += f"${i},"
                    args.append(val)
                    i += 1
        self.sql = f"INSERT INTO {table.__name__}s({sort_names[:-1]}) VALUES({sort_vars[:-1]});"
        self.table = table
        self.args = tuple(args)


class Select:
    def __init__(self, table, **kwargs):
        if len(kwargs) == 0:
            command = f"""SELECT * FROM {table.__name__}s WHERE TRUE;"""
            args = []
        else:
            filter_db = str()
            i = 1
            args = []
            for name, value in kwargs.items():
                filter_db += f"""{name}=${i} AND """
                args.append(value)
                i += 1
            filter_db = filter_db[:-5]
            command = f"""SELECT * FROM {table.__name__}s WHERE {filter_db};"""

        self.sql = command
        self.table = table
        self.args = tuple(args)


class DropTable:
    def __init__(self, table):
        self.sql = f"DROP TABLE {table.__name__}s;"
        self.table = table
        self.args = ()


class Delete:
    def __init__(self, table, is_found: bool, **kwargs):
        args = []
        if is_found:
            command = f"DELETE FROM {table.__bigclass__.__name__}s WHERE "
            filter_db = str()
            i = 1
            for name, value in table.__dict__.items():
                if not name.startswith("__") and value is not None:
                    filter_db += f"""{name}=${i} AND """
                    args.append(value)
                    i += 1
            filter_db = filter_db[:-5]
            command += filter_db + ";"
        else:
            if len(kwargs) != 0:
                filter_db = str()
                i = 1
                args = []
                for name, value in kwargs.items():
                    filter_db += f"""{name}=${i} AND """
                    args.append(value)
                    i += 1
                filter_db = filter_db[:-5]
                command = f"DELETE FROM {table.__name__}s WHERE {filter_db};"
            else:
                command = f"DELETE FROM {table.__name__}s WHERE TRUE;"
        self.sql = command
        self.args = tuple(args)
        self.table = table


class Update:
    def __init__(self, table, is_found: bool, updating: dict, **kwargs):
        if is_found:
            command = f"UPDATE {table.__bigclass__.__name__}s SET "
            filter_db = str()
            i = 1
            args = []
            edit_db = str()
            edit_names = []
            for name, value in kwargs.items():
                edit_db += f"{name}=${i}"
                edit_names.append(name)
                args.append(value)
                i += 1
                break
            for name, value in table.__dict__.items():
                if not name.startswith("__") and name not in edit_names and value is not None:
                    filter_db += f"""{name}=${i} AND """
                    args.append(value)
                    i += 1
            filter_db = filter_db[:-5]
            command += edit_db + " WHERE " + filter_db + ";"
            self.sql = command
        else:
            command = f"UPDATE {table.__name__}s SET "
            filter_db = str()
            args = []
            edit_db = str()
            i = 1
            for name, value in updating.items():
                if type(name) == Column:
                    name = name.__namecolumn__
                    edit_db += f"{name}=${i}, "
                    args.append(value)
                    i += 1

            if len(kwargs) != 0:
                for name, value in kwargs.items():
                    filter_db += f"""{name}=${i} AND """
                    args.append(value)
                    i += 1
                filter_db = filter_db[:-5]
                command += edit_db[:-2] + " WHERE " + filter_db + ";"
                self.sql = command
            else:
                command += edit_db[:-2] + " WHERE " + "TRUE;"
                self.sql = command
        self.args = tuple(args)
        self.table = table
