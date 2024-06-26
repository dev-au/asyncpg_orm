from typing import Union, Optional, List, Any

from .serializer import SelectedTable
from .sql_commands import *


class Table:

    @classmethod
    def connect_to_database(cls, database):
        cls.__database__ = database
        return cls

    @classmethod
    async def create_table(cls) -> str:
        sql = CreateTable(cls)
        return await cls.__database__.__cursor__(sql.sql, *sql.args, execute=True)

    @classmethod
    async def add_new(cls, **kwargs) -> str:
        sql = NewRow(cls, **kwargs)
        return await cls.__database__.__cursor__(sql.sql, *sql.args, execute=True)

    @classmethod
    async def select(cls, **kwargs) -> SelectedTable:
        sql = Select(cls, **kwargs)

        result = await cls.__database__.__cursor__(sql.sql, *sql.args, fetchrow=True)
        if result is None:
            return None
        i = 0
        new_table = SelectedTable()
        for name, value in sql.table.__dict__.items():
            if not name.startswith("__"):
                setattr(new_table, name, result[i])
                i += 1
        new_table.__database__ = cls.__database__
        new_table.__bigclass__ = sql.table
        return new_table

    @classmethod
    async def select_all(cls, **kwargs) -> List[SelectedTable]:
        sql = Select(cls, **kwargs)
        results = await cls.__database__.__cursor__(sql.sql, *sql.args, fetch=True)
        if len(results) == 0:
            return []

        all_tables = []
        for result in results:
            i = 0
            new_table = SelectedTable()
            for name, value in sql.table.__dict__.items():
                if not name.startswith("__"):
                    setattr(new_table, name, result[i])
                    i += 1
            new_table.__database__ = cls.__database__
            new_table.__bigclass__ = sql.table
            all_tables.append(new_table)

        return all_tables

    @classmethod
    async def drop_table(cls) -> str:
        sql = DropTable(cls)

        return await cls.__database__.__cursor__(sql.sql, *sql.args, execute=True)

    @classmethod
    async def delete(cls, **kwargs) -> str:
        sql = Delete(cls, is_found=False, **kwargs)
        result = await cls.__database__.__cursor__(sql.sql, *sql.args, execute=True)
        count = int(str(result).split(" ")[1])
        if count == 0:
            raise AttributeError("Row was already deleted or not found")
        return result

    @classmethod
    async def update(cls, updating: dict, **kwargs) -> str:
        sql = Update(cls, is_found=False, updating=updating, **kwargs)
        result = await cls.__database__.__cursor__(sql.sql, *sql.args, execute=True)
        count = int(str(result).split(" ")[1])
        if count == 0:
            raise AttributeError("Row not found")
        return result
