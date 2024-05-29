import sqlite3
import os

class UserSqliteConnection:
    def __init__(self, db_path, db_name):
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True) # Make sure the directory exists
        self.conn = sqlite3.connect(os.path.join(db_path, db_name))
        self.cursor = self.conn.cursor()
        self.init_create()

    def init_create(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_id TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS summarization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_id TEXT NOT NULL,
            summarization TEXT 
        )
        ''')
        self.conn.commit()

    def insert_user(self, line_id, query, response):
        self.cursor.execute('''
        INSERT INTO users (line_id, query, response) VALUES (?, ?, ?)
        ''', (line_id, query, response))
        self.conn.commit()
        
    def insert_summarization(self, line_id, summarization):
        self.cursor.execute('''
        INSERT INTO summarization (line_id, summarization) VALUES (?, ?)
        ''', (line_id, summarization))
        self.conn.commit()
        
    def update_summarization(self, line_id, summarization):
        self.cursor.execute('''
        UPDATE summarization SET summarization = ? WHERE line_id = ?
        ''', (summarization, line_id))
        self.conn.commit()

    def fetch_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def fetch_all_by_user_line_id(self, line_id):
        self.cursor.execute('SELECT * FROM users WHERE line_id = ?', (line_id,))
        return self.cursor.fetchall()

    def fetch_all_summarization(self):
        self.cursor.execute('SELECT * FROM summarization')
        return self.cursor.fetchall()
    
    def fetch_all_by_summarization_line_id(self, line_id):
        self.cursor.execute('SELECT * FROM summarization WHERE line_id = ?', (line_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    db_manager = UserSqliteConnection(db_path="./database/", db_name="user_info.db")
    
    # 查詢所有 users 資料
    users = db_manager.fetch_all_users()
    for user in users:
        print(user)

    # # 根據 line_id 查詢 users 資料
    # users_by_line_id = db_manager.fetch_all_by_user_line_id("123")
    # for user in users_by_line_id:
    #     print(user)

    # # 查詢所有 summarization 資料
    # summarizations = db_manager.fetch_all_summarization()
    # for summarization in summarizations:
    #     print(summarization)

    # # 根據 line_id 查詢 summarization 資料
    # summarizations_by_line_id = db_manager.fetch_all_by_summarization_line_id("123")
    # for summarization in summarizations_by_line_id:
    #     print(summarization)

    # 關閉資料庫連線
    db_manager.close()
