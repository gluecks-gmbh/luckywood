"""
Helper class for mysql database usage
"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Frederik Glücks - Glücks GmbH"

# Built-in/Generic Imports
import os
import logging
import hashlib
import mysql.connector
import mysql.connector.cursor

# own libs
from .data_caching import DataCaching


class Database:
    """
    Helper class for mysql database usage
    """
    __cnx: mysql.connector = None
    __cursor: mysql.connector.cursor = None

    @staticmethod
    def open():
        """
        Creates a database connection by using environment vars.

        Environment vars:
        RDS_HOST = database host, default value "localhost"
        RDS_HOST_PORT = database port, default value "3306"
        RDS_DATABASE = database name, default value ""
        RDS_USERNAME = username, default value ""
        RDS_PASSWORD = password, default value ""

        :return: none
        """
        host: str = os.getenv('RDS_HOST', 'localhost')
        port: str = os.getenv('RDS_HOST_PORT', '3306')
        database: str = os.getenv('RDS_DATABASE', 'None')
        username: str = os.getenv('RDS_USERNAME', '')
        password: str = os.getenv('RDS_PASSWORD', '')

        Database.__cnx = mysql.connector.connect(username=username,
                                                 password=password,
                                                 host=host,
                                                 database=database,
                                                 port=port)

        Database.__cnx.autocommit = True

        Database.__cursor = Database.__cnx.cursor(dictionary=True)

    @staticmethod
    def close():
        """
        Closes the database connection

        :return: none
        """
        if Database.__cnx:
            Database.__cursor.close()
            Database.__cnx.close()

    @staticmethod
    def fetchall_without_cache(query: str, param: tuple = ()) -> dict:
        """
        Returns the result of the query as dict.

        The luckywood DataCaching class will NOT be used.

        :param query: str
        :param param: tuple
        :return: dict
        """
        if Database.__cursor is None:
            Database.open()

        if query == "":
            raise RuntimeError("Empty query")

        Database.__cursor.execute(query, param)

        return Database.__cursor.fetchall()

    @staticmethod
    def fetchall_with_cache(query: str, param: tuple = ()) -> dict:
        """
        Returns the result of the query as dict by using the luckywood DataCaching
        class.

        :param query: str
        :param param: tuple
        :return: dict
        """
        tuple_str: str = ""

        for var in param:
            tuple_str += str(var)

        query_hash: str = hashlib.md5(query.encode() + tuple_str.encode()).hexdigest()
        cache_name = "database"

        result_set = DataCaching.get(cache_name, query_hash)

        if len(result_set) == 0:
            logging.info("Query load from database")
            result_set = Database.fetchall_without_cache(query, param)
            DataCaching.set(cache_name, query_hash, result_set)
        else:
            logging.info("Query load from cache")

        return result_set

    @staticmethod
    def query(query: str, param: tuple = ()) -> int:
        """
        Runs a query and returns the number of affected rows

        :param query: str
        :param param: tuple
        :return: int
        """
        if Database.__cursor is None:
            Database.open()

        Database.__cursor.execute(query, param)

        if Database.__cursor.fetchwarnings() is not None:
            logging.info(Database.__cursor.fetchwarnings())

        return Database.__cursor.rowcount
