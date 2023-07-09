# -*- coding:utf-8- -*-
"""
Author:Yang Sheng-rong
Date:2023年07月09日
Email:3118393236@qq.com
"""
from typing import Union


class Field:
    field_type_list = [
        'CHAR', 'VARCHAR', "TINYTEXT", "TEXT", "LONGTEXT", "TINYBLOB", "BLOB", "LONGBLOB", "TINYINT",
        "SMALLINT", "INT", "BIGINT", "FLOAT", "DOUBLE", "YEAR", "TIME", "DATE", "DATETIME", "TIMESTAMP"
    ]
    field_length_dict = {
        "CHAR": [0, 255],
        "VARCHAR": [0, 65535],
        "TINYTEXT": [0, 255],
        "TEXT": [0, 65535],
        "LONGTEXT": [0, 4294967295],
        "TINYBLOB": [0, 255],
        "BLOB": [0, 65535],
        "LONGBLOB": [0, 4294967295],
        "TINYINT": "",
        "SMALLINT": "",
        "INT": "",
        "BIGINT": "",
        "FLOAT": [0, 53],
        "DOUBLE": "",
        "YEAR": "",
        "TIME": "",
        "DATE": "",
        "DATETIME": "",
        "TIMESTAMP": ""
    }

    def __init__(self, length: Union[int, bool], primary: bool = False, null: bool = False, unique: bool = False,
                 verbose_name: str = None):
        self.field_type = None
        self.length = length
        self.primary = primary
        self.null = null
        self.unique = unique
        self.verbose_name = verbose_name

    def save(self):
        if self.check_field_length():
            return self.__dict__
        return False

    def check_field_length(self):
        if self.field_type in self.field_type_list:
            if isinstance(self.field_length_dict[self.field_type], list):
                left = self.field_length_dict[self.field_type][0]
                right = self.field_length_dict[self.field_type][1]
                if left <= self.length <= right:
                    return True
            elif isinstance(self.field_length_dict[self.field_type], str):
                return True
            return False
        return False


class CharField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'CHAR'


class VarCharField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'VARCHAR'


class TinyTexTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'TINYTEXT'


class TextField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'TEXT'


class LongTextField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'LONGTEXT'


class TinyBlobField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'TINYBLOB'


class BlobField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'BLOB'


class LongBlobField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'LONGBLOB'


class TINYINTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'TINYINT'
        self.length = False


class SMALLINTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'SMALLINT'
        self.length = False


class MEDIUMINTTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'MEDIUMINT'
        self.length = False


class INTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'INT'
        self.length = False


class BIGINTField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'BIGINT'
        self.length = False


class FLOATField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.field_type = 'FLOAT'


class DOUBLEField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'DOUBLE'
        self.length = False


class YEARField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'YEAR'
        self.length = False


class TIMEField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'TIME'
        self.length = False


class DATEField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'DATE'
        self.length = False


class DATETIMEField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'DATETIME'
        self.length = False


class TIMESTAMPField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.length
        self.field_type = 'TIMESTAMP'
        self.length = False
