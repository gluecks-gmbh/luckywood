"""
Objekt für die Nutzung einer MySQL-Datenbank
"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = ""

# Built-in/Generic Imports
import os
import hashlib
import mysql.connector
import mysql.connector.cursor

# own libs
from .data_caching import DataCaching


class Database:
    """
    MySQL Abstraktion
    """
    __cnx: mysql.connector = None
    __cursor: mysql.connector.cursor = None

    @staticmethod
    def open():
        """
        Verbindung zur MySQL Datenbank wird an Hand von Environment Variablen aufgebaut
        :return: none
        """
        host: str = os.getenv('RDS_HOST', 'None')
        port: str = os.getenv('RDS_HOST_PORT', 'None')
        database: str = os.getenv('RDS_DATABASE', 'None')
        username: str = os.getenv('RDS_USERNAME', 'None')
        password: str = os.getenv('RDS_PASSWORD', 'None')

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
        Datenbank-Verbindung wird geschlossen
        :return: none
        """
        if Database.__cnx:
            Database.__cursor.close()
            Database.__cnx.close()

    @staticmethod
    def fetchall_without_cache(query: str, param: tuple = ()) -> dict:
        """
        Liefert alle Ergebnisse eines queries als dict zurück.

        Der Interne Cache wird nicht genutzt.

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
        tuple_str: str = ""

        for var in param:
            tuple_str += str(var)

        query_hash: str = hashlib.md5(query.encode() + tuple_str.encode()).hexdigest()
        cache_name = "database"

        result_set = DataCaching.get(cache_name, query_hash)

        if len(result_set) == 0:
            result_set = Database.fetchall_without_cache(query, param)
            DataCaching.set(cache_name, query_hash, result_set)

        return result_set
