class Serial:
    __sqloperation__: str = "SERIAL"


class BigInteger:
    __sqloperation__: str = 'BIGINT'


class String:
    __sqloperation__: str = "VARCHAR"

    def __init__(self, max_length: int = None):
        if max_length != None and type(max_length) == int:
            self.__sqloperation__ += f" ({max_length})"


class Float:
    __sqloperation__: str = "FLOAT"


class Integer:
    __sqloperation__: str = "INTEGER"


class Text:
    __sqloperation__: str = "TEXT"

    def __init__(self, max_length: int = None):
        if max_length != None and type(max_length) == int:
            self.__sqloperation__ += f" ({max_length})"


class Boolean:
    __sqloperation__: str = "BOOLEAN"


class IntArray:
    __sqloperation__: str = "INT ARRAY"


class StringArray:
    __sqloperation__: str = "VARCHAR ARRAY"


class Json:
    __sqloperation__: str = "JSON"
