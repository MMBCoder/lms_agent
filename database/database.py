import sqlite3
from config.settings import DATABASE_PATH
from database.schema import COURSES_TABLE, CONTENT_TABLE, PROGRESS_TABLE

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.conn = sqlite3.connect(db_path)

    def initialize(self):
        cursor = self.conn.cursor()
        cursor.execute(COURSES_TABLE)
        cursor.execute(CONTENT_TABLE)
        cursor.execute(PROGRESS_TABLE)
        self.conn.commit()
