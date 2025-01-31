from . import Database

class BackendEndpoint:
    def __init__(self):
        self.__sql = Database()

    def get_messages_table(self):
        return self.__sql.fetch_query('SELECT * FROM messages')

    def get_users_table(self):
        return self.__sql.fetch_query('SELECT * FROM users')

    def admin_query(self, _query):
        return self.__sql.fetch_query(_query=_query)