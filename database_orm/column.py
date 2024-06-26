from typing import Union
from .data_types import *


class Column:
    __sqloperation__: str
    data_type: Union[Serial, String, Integer, Text, Boolean, IntArray, StringArray, Float, BigInteger]
    primary_key: bool = False
    not_null: bool = False
    unique: bool = False

    def __init__(self, data_type: Union[Serial, String, Integer, Text, Boolean, IntArray, StringArray, Float,
    BigInteger],
                 not_null: bool = False,
                 unique: bool = False,
                 primary_key: bool = False):
        if type(data_type) not in [Serial, String, Integer, Text, Boolean, IntArray, StringArray, Float, BigInteger]:
            raise TypeError("data_type can be only str, int, float, bool, list, dict types")
        elif type(not_null) != bool:
            raise TypeError("not_null can be only boolean type")
        elif type(primary_key) != bool:
            raise TypeError("primary_key can be only boolean type")
        elif type(unique) != bool:
            raise TypeError("unique can be only boolean type")
        else:
            self.data_type = data_type
            self.__sqloperation__ = data_type.__sqloperation__
            if not_null:
                self.__sqloperation__ += " NOT NULL"
                self.not_null = True
            if unique:
                self.__sqloperation__ += " UNIQUE"
                self.unique = unique
            else:
                if primary_key:
                    self.__sqloperation__ += " PRIMARY KEY"
                    self.primary_key = True
