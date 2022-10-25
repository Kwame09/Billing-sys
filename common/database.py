#!python3
# -*- coding: utf-8 -*-
# @Date    : 2022-07-22 11:42:39
# @Author  : Amos Amissah (theonlyamos@gmai.com)
# @Link    : link
# @Version : 1.0.0

import os
from mysql import connector
from constants import HOST, PASSWORD, USER


class Database:
    db = None
    cursor = None

    @staticmethod
    def initialize():
        db = connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database="Billing_System",
            auth_plugin='mysql_native_password'
        )

        cursor = db.cursor(buffered=True, dictionary=True)
        Database.db = db
        Database.cursor = cursor
    
    @staticmethod
    def insert(table: str, data: dict):

        query = f'INSERT INTO {table}('
        query += ', '.join(data.keys())
        query += ") VALUES('"

        values = [str(val) for val in data.values()]
        query += "','".join(values)
        query += "')"
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return str(Database.cursor.lastrowid)

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def update(table: str, id: int, data: dict):

        query = f'UPDATE {table} SET'
        for key in data.keys():
            query += f" {key}='{data[key]}',"
        
        query = query.rstrip(',')
        
        query += f" WHERE id={id}"

        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return str(Database.cursor.lastrowid)

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def find(table: str, params: dict = {}):
        query = f'SELECT * FROM {table}'

        if len(params.keys()):
            query += ' WHERE '
            for key in params.keys():
                query += f"{key}='{params[key]}'"
        
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return [x for x in Database.cursor.fetchall()]

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def find_one(table: str, params: dict = {}):
        query = f'SELECT * FROM {table}'
        
        if len(params.keys()):
            query += ' WHERE '
            for key in params.keys():
                query += f"{key}='{params[key]}'"
        
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            resp = [x for x in Database.cursor.fetchall()]
            return resp[0]

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def count(table: str, params: dict = {}):
        query = f'SELECT COUNT(*) as count FROM {table}'

        if len(params.keys()):
            query += ' WHERE '
            for key in params.keys():
                query += f"{key}='{params[key]}'"
        
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return Database.cursor.fetchall()[0]['count']

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
        
    @staticmethod
    def sum(table: str, column: str):
        query = f'SELECT SUM({column}) as sum FROM {table}'
        
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return Database.cursor.fetchall()[0]['sum']

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def query(query: str):
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return [x for x in Database.cursor.fetchall()]

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    @staticmethod
    def delete(table: str, id: int):

        query = f'DELETE FROM {table} WHERE id={id}'
        
        try:
            Database.cursor.execute(query, None)
            Database.db.commit()

            return str(Database.cursor.lastrowid)

        except Exception as e:
            return {'status': 'Error', 'message': str(e)}