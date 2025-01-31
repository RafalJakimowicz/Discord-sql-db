import os
import sqlite3
import threading

class Database:
    __database_file_directory = 'datafiles'
    __attachments_directory = os.path.join(__database_file_directory,'attachments')

    def __init__(self):
        self.__filename = 'database.db'

        if not os.path.exists(self.__database_file_directory):
            os.makedirs(self.__database_file_directory)
        if not os.path.exists(self.__attachments_directory):
            os.makedirs(self.__attachments_directory)

        self.__connection = sqlite3.connect(os.path.join(self.__database_file_directory, self.__filename), check_same_thread=False)
        self.__db = self.__connection.cursor()
        #table for messeges
        self.__db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
        id INT UNIQUE,
        guild TEXT NOT NULL,
        channel TEXT NOT NULL,
        username TEXT NOT NULL,
        creationtime TEXT NOT NULL,
        attachment TEXT,
        content TEXT)
        ''')
        #table for users
        self.__db.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INT UNIQUE,
        name TEXT NOT NULL,
        jointime TEXT NOT NULL,
        present INT NOT NULL)
        ''')
        self.__connection.commit()
        self.lock = threading.Lock()

    def __del__(self):
        self.__connection.close()

    def attachment_path(self) -> str:
        return self.__attachments_directory

    def exec_query(self,_query, _params=()):
        from . import logger
        with self.lock:
            try:
                self.__db.execute(_query, _params)
                self.__connection.commit()
            except sqlite3.Error as e:
                self.__connection.rollback()
                logger.error(f'{self.exec_query.__name__}: {e}')

    def fetch_query(self, _query, _params=()):
        from . import logger
        try:
            self.__db.execute(_query, _params)
            return self.__db.fetchall()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.fetch_query.__name__}: {e}')