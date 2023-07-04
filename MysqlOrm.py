# -*- coding:utf-8- -*-
"""
Author:Yang Sheng-rong
Date:2023年07月03日
Email:3118393236@qq.com
"""

import pymysql
from typing import Union, Any


class MysqlOrm:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.sql = None
        self.table = None
        self.cursor = None
        self.dict = {
            "__gte": '>=',
            '__gt': '>',
            "__lte": '<=',
            "__lt": '<',
            "__ne": '!='
        }
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.create_cursor()

    def get_fields(self, table) -> list:
        sql = f"""SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION;"""
        self.execute_sql(sql)
        return list(self.cursor.fetchall())

    def filter_rule(self, item) -> dict:
        dic = {}
        dict_keys = list(self.dict.keys())
        for key in dict_keys:
            if key in item:
                dic = {item.replace(key, ''): self.dict[key]}
                break
            else:
                dic = {item: "="}
        return dic

    def create_cursor(self) -> Any:
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def objects(self, table):
        self.table = table
        return self

    def insert(self, **kwargs):
        sql = f'''insert into {self.table} set '''
        key_list = list(kwargs.keys())
        value_list = list(kwargs.values())
        for index in range(len(key_list)):
            if index + 1 < len(key_list):
                sql += f'''{key_list[index]} = '{value_list[index]}', '''
            else:
                sql += f'''{key_list[index]} = '{value_list[index]}';'''
        self.sql = sql
        return self

    def delete(self, by: str, by_value: str):
        sql = f'''DELETE FROM {self.table} WHERE {by} = '{by_value}'; '''
        self.sql = sql
        print(sql)
        return self

    def update(self, by: str, by_value: str, **kwargs):
        sql = f'''UPDATE {self.table} SET '''
        sql_end = f''' WHERE {by} = '{by_value}';'''
        key_list = list(kwargs.keys())
        value_list = list(kwargs.values())
        for index in range(len(key_list)):
            if index + 1 < len(key_list):
                sql += f'''{key_list[index]} = '{value_list[index]}', '''
            else:
                sql += f'''{key_list[index]} = '{value_list[index]}' '''
        sql = sql + sql_end
        self.sql = sql
        return self

    def select(self, **kwargs) -> object:
        sql = f'''select * from {self.table} where '''
        key_list = list(kwargs.keys())
        key_list = list(map(self.filter_rule, key_list))
        value_list = list(kwargs.values())
        for index in range(len(key_list)):
            key = list(key_list[index].keys())[0]
            rule = list(key_list[index].values())[0]
            value = "'" + str(value_list[index]) + "'"
            if index + 1 < len(key_list):
                sql += f'''{key} {rule} {value} and '''
            else:
                sql += f'''{key} {rule} {value}'''
        self.sql = sql
        return self

    def all(self) -> object:
        sql = f'''select * from {self.table}'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def save(self):
        self.cursor.execute(self.sql)
        self.connection.commit()

    def execute_sql(self, sql) -> Any:
        self.cursor.execute(sql)
        return self

    def result(self, is_dict: bool = None) -> list:
        self.cursor.execute(self.sql)
        sql_data_list = self.cursor.fetchall()
        data_list = []
        if is_dict:
            fields = list(map(lambda item: item[0], self.get_fields(self.table)))
            for sql_data in sql_data_list:
                data_dict = {}
                for i in range(len(fields)):
                    data_dict[fields[i]] = sql_data[i]
                data_list.append(data_dict)
            return data_list
        return sql_data_list
