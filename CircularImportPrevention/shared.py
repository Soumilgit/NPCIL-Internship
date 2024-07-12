import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('users.db')  # Connect to a file-based database
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def create_table(conn):
    try:
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
        conn.commit()
    except Error as e:
        print(e)

def insert_user(conn, user):
    sql = '''INSERT OR IGNORE INTO users(username,password)
             VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, (user.username, user.password,))
    conn.commit()
    return cur.lastrowid

def select_user(conn, username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
    rows = cur.fetchall()
    return rows








class UserManager:
    def __init__(self):
        self.users_list = []

    # Add other methods of UserManager here
