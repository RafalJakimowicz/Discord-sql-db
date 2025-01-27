import os
import sqlite3
import logging

class Database:

    __database_file_directory = 'datafiles'
    __attachments_directory = os.path.join(__database_file_directory,'attachments')

    def __init__(self, _filename: str = 'database.db'):
        if not os.path.exists(self.__database_file_directory):
            os.makedirs(self.__database_file_directory)
        if not os.path.exists(self.__attachments_directory):
            os.makedirs(self.__attachments_directory)

        #setup logging
        logging.basicConfig(
            filename='database.log',
            format='%(lavelname)s: %(asctime)s: %(messege)s',
            datefmt='%d-%m-%Y %H:%M:%S')

        self.__connection = sqlite3.connect(_filename)
        self.__db = self.__connection.cursor()
        #table for messeges
        self.__db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
        id INT,
        guild TEXT NOT NULL,
        channel TEXT NOT NULL,
        username TEXT NOT NULL,
        creationtime TEXT NOT NULL,
        attachment TEXT,
        content TEXT
        )
        ''')
        #table for users
        self.__db.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INT UNIQUE,
        name TEXT NOT NULL,
        jointime TEXT NOT NULL,
        present INT NOT NULL CHECK (present in (0,1))
        )
        ''')

    def attachment_path(self) -> str:
        return self.__attachments_directory

    async def save_message(self, _id: int, _guild: str, _channel: str, _username: str, _creationtime: str, _attachment: str, _content: str):
        try:
            self.__db.execute('INSERT INTO messeges (id, guild, channel, username, creationtime, attachment, content) VALUES (?,?,?,?,?,?,?)', 
            (_id, _guild, _channel, _username, _creationtime, _attachment, _content))
            self.__connection.commit()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logging.error(f'{self.save_message.__name__}: {e}')

    async def get_query_by_name(self, _name) -> list:
        try:
            self.__db.execute('SELECT * FROM messages WHERE username=?', (_name))
        except sqlite3.Error as e:
            self.__connection.rollback()
            logging.error(f'{self.save_message.__name__}: {e}')
        finally:
            return self.__db.fetchall()

