from .sql_commands import *


class SelectedTable:
    async def delete(self) -> None:
        try:
            sql = Delete(self, is_found=True)
            result = await self.__database__.__cursor__(sql.sql, *sql.args, execute=True)
            count = int(str(result).split(" ")[1])
            if count == 0:
                raise AttributeError("Row was already deleted or not found")
            self.__dict__.clear()
        except:
            raise AttributeError("Row was already deleted or not found")

    async def update(self, **kwargs) -> None:
        try:
            sql = Update(self, is_found=True, updating_column=None, updating_value=None, **kwargs)
            result = await self.__database__.__cursor__(sql.sql, *sql.args, execute=True)
            count = int(str(result).split(" ")[1])
            if count == 0:
                raise AttributeError("Row not found")
            for name, value in kwargs.items():
                setattr(self, name, value)
        except:
            raise AttributeError("Row not found")
