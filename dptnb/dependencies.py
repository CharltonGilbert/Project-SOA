from sqlite3 import Cursor
from unittest import result
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def regis(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount > 0):
            cursor.close()
            result.append("Username is not registered")
            return result
        else:
            sql = "INSERT INTO user VALUES(0, '{}', '{}')".format(a, b)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registered Successfully")
            return result
        
    def login(self, a, b):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * from user where username = '{}'".format(a)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("Username is not registered")
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == b):
                cursor.close()
                result.append("Login Success")
                return 1
            else:
                cursor.close()
                result.append("Incorrect password")
                return 0
    
    def getu(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'username': row['username'],
                'password': row['password']
            })
        cursor.close()
        return result

    def get_news(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE date >= DATE_SUB(curdate(), INTERVAL 30 DAY)"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'category': row['category'],
                'date': row['date']
            })
        cursor.close()
        return result

    def get_news_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'category': row['category'],
                'date': row['date']
            })
        cursor.close()
        return result

    def insert_news(self, category, date):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "INSERT INTO news VALUES(0, '{}', '{}')".format(category, date)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        result.append("News successfully added")
        return result

    def edit_news(self, id, category, date):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "UPDATE news SET category = '{}', date = '{}' WHERE id = {}".format(category, date, id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        result.append("News has been updated")
        return result

    def delete_news(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "DELETE FROM news WHERE id = {}".format(id)
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        result.append("News Deleted")
        return result
    
    def __del__(self):
        self.connection.close()




class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='departmentnews',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
