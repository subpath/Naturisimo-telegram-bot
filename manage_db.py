import sqlite3
from datetime import datetime

from get_offers import send_notifications
from config import TOKEN

class DataHandler:
    def __init__(self):
        self.db_name = 'offers.db'
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name: str, column_name: str):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {}(created_at INTEGER, {} TEXT)".format(table_name, column_name))

    def write_to_table(self, table: str, created_at: int, value: str):
        self.cursor.execute("INSERT INTO {} VALUES({},'{}')".format(table, created_at, value))
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def read_from_table(self, table: str):
        self.cursor.execute('SELECT * FROM {}'.format(table))
        data = self.cursor.fetchall()
        values = [i[1] for i in data]
        return values

    def check_updates(self, table: str, value: str):
        available_values = self.read_from_table(table)
        if value not in available_values:
            self.write_to_table(table, int(datetime.utcnow().strftime('%s')), value)
            if table == 'offers':
                users = self.read_from_table('users')
                for user in users:
                    message = "Wow! New offer : {}".format(value)
                    send_notifications(TOKEN, user, message)
            return True

    def delete_user(self, table: str, value: str):
        self.cursor.execute("DELETE FROM {} WHERE chat_id = {};".format(table, value))
        self.connection.commit()
