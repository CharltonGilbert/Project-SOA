import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import itertools
from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def upload_file(self, path):
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            sql = "INSERT INTO files VALUES (DEFAULT, '{}')".format(path)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            print("Record inserted successfully into files table")
        except mysql.connector.Error as error:
            print("Failed to insert into files table {}".format(error))
            return False
        return True

    def download_file(self, id):
        try:
            cursor = self.connection.cursor(dictionary=True, buffered=True)
            sql = "SELECT * FROM files WHERE id = {}".format(id)
            cursor.execute(sql)
            file = cursor.fetchone()
            cursor.close()
            print("Record fetched successfully from files table")
        except mysql.connector.Error as error:
            print("Failed to fetch record from files table {}".format(error))
            return False
        return file

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
                database='simplecloudstorage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
