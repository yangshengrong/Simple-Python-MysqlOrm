# -*- coding:utf-8- -*-
"""
Author:Yang Sheng-rong
Date:2023年07月09日
Email:3118393236@qq.com
"""
import pymysql
from typing import Any
import re


class ConnectDataBase:

    def __init__(self, host, user, password, database):
        self.connection = None
        self.cursor = None
        self.sql = None
        self.table = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._create_cursor()

    def to_orm(self):
        return {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "database": self.database
        }

    def _create_cursor(self) -> Any:
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def _build_field_sql(self, model) -> list:
        print(model.__annotations__)
        self.table_name = re.findall("<attribute '__dict__' of '(.*?)' objects>", str(model.__dict__['__dict__']))[0]
        self.model: dict = model.__annotations__
        field_list = list(self.model.items())
        field_sql_list = []
        for index in range(len(field_list)):
            field = field_list[index]
            field_name = field[0]
            field_type = field[1]['field_type']
            field_length = field[1]['length']
            primary = field[1]['primary']
            null = field[1]['null']
            unique = field[1]['unique']
            verbose_name = field[1]['verbose_name']
            if field_length:
                field_type = f'{field_type}({field_length})'
            if primary:
                primary = 'PRIMARY KEY'
            else:
                primary = None
            if unique:
                unique = "UNIQUE"
            else:
                unique = None
            if null:
                null = "NULL"
            else:
                null = "NOT NULL"
            if verbose_name:
                verbose_name = f"COMMENT '{verbose_name}'"
            else:
                verbose_name = None
            field_sql = f'{field_name} {field_type} {primary} {unique} {null} {verbose_name},'.replace(' None', '')
            if index + 1 == len(field_list):
                field_sql = field_sql.replace(',', '')
            field_sql_list.append(field_sql)
        return field_sql_list

    def create_table(self, model: object):
        field_sql_list = self._build_field_sql(model)
        field_part = ''
        for field_sql in field_sql_list:
            field_part += field_sql + '\n'
        field_part = '(\n' + field_part + ')'
        self.sql = f"CREATE TABLE {self.table_name} {field_part} default charset=utf8;"
        self.cursor.execute(self.sql)
        self.connection.commit()
