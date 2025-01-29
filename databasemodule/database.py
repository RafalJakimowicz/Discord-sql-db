import os
import sqlite3

class Database:
    __database_file_directory = 'datafiles'
    __attachments_directory = os.path.join(__database_file_directory,'attachments')

    def __init__(self, _filename: str = 'database.db'):


        if not os.path.exists(self.__database_file_directory):
            os.makedirs(self.__database_file_directory)
        if not os.path.exists(self.__attachments_directory):
            os.makedirs(self.__attachments_directory)

        self.__connection = sqlite3.connect(os.path.join(self.__database_file_directory, _filename))
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

    def attachment_path(self) -> str:
        return self.__attachments_directory

    def save_message(self, _id: int, _guild: str, _channel: str, _username: str, _creationtime: str, _attachment: str, _content: str):
        from . import logger
        try:
            self.__db.execute('INSERT INTO messages (id, guild, channel, username, creationtime, attachment, content) VALUES (?,?,?,?,?,?,?)', 
            (_id, _guild, _channel, _username, _creationtime, _attachment, _content))
            self.__connection.commit()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.save_message.__name__}: {e}')

    def get_query_by_name(self, _name) -> list:
        from . import logger
        try:
            self.__db.execute('''SELECT * FROM messages WHERE username = ?''', (_name,))
            return self.__db.fetchall()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.save_message.__name__}: {e}')

    def save_user(self, _id: int, _name: str, _jointime: str, _present: int):
        from . import logger
        try:
            self.__db.execute('INSERT INTO users (id, name, jointime, present) VALUES (?,?,?,?)', 
            (_id, _name, _jointime, _present))
            
            self.__connection.commit()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.save_message.__name__}: {e}')

    def update_removed_user(self, _id: int):
        from . import logger
        try:
            self.__db.execute('UPDATE users SET present = 0 WHERE id = ?',(_id,))
            self.__connection.commit()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.save_message.__name__}: {e}')

    def export_database(self, _table: str) -> list:
        from . import logger   
        try:
            if not _table.isidentifier():
                raise sqlite3.Error('Incorect input')

            self.__db.execute(f'SELECT * FROM {_table}')
            return self.__db.fetchall()
        except sqlite3.Error as e:
            self.__connection.rollback()
            logger.error(f'{self.save_message.__name__}: {e}')