from . import Database

class BotEndpoint:
    def __init__(self):
        self.__sql = Database()

    def save_message(self, _id: int, _guild: str, _channel: str, _username: str, _creationtime: str, _attachment: str, _content: str):
        self.__sql.exec_query('INSERT INTO messages (id, guild, channel, username, creationtime, attachment, content) VALUES (?,?,?,?,?,?,?)',
        (_id, _guild, _channel, _username, _creationtime, _attachment, _content))

    def get_query_by_name(self, _name) -> list:
        return self.__sql.fetch_query('SELECT * FROM messages WHERE username = ?',(_name,))

    def save_user(self, _id: int, _name: str, _jointime: str, _present: int):
        self.__sql.exec_query('INSERT INTO users (id, name, jointime, present) VALUES (?,?,?,?)',(_id, _name, _jointime, _present))

    def update_removed_user(self, _id: int):
        self.__sql.exec_query('UPDATE users SET present = 0 WHERE id = ?',(_id,))

    def export_database(self, _table: str) -> list:

        if not _table.isidentifier():
                return None

        return self.__sql.fetch_query(f'SELECT * FROM {_table}')

