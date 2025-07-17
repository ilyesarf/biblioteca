import psycopg2
from psycopg2 import sql

class DB:
    def __init__(self, host, port, user, password, dbname):
        self.con = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        self.cur = self.con.cursor()

        # Create tables if not exists
        self.create_db()

    def create_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_hash TEXT PRIMARY KEY
            )
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS store (
                user_hash TEXT,
                book_id TEXT,
                book_title TEXT,
                PRIMARY KEY (user_hash, book_id),
                FOREIGN KEY (user_hash) REFERENCES users(user_hash) ON DELETE CASCADE
            )
        """)
        self.con.commit()

    #Users
    def get_users(self):
        query = "SELECT user_hash FROM users"
        res = self.cur.execute(query)
        
        return res.fetchall()
    
    def add_user(self, user_hash):
        query = "INSERT INTO users VALUES (%s)"
        self.cur.execute(query, (user_hash,))
        self.con.commit()        

    def is_user(self, user_hash):
        query = "SELECT user_hash FROM users WHERE user_hash=%s"
        self.cur.execute(query, (user_hash,))
        res = self.cur.fetchall()
        return len(res) > 0

    def delete_user(self, user_hash):
        query = "DELETE FROM users WHERE user_hash=%s"
        self.cur.execute(query, (user_hash,))
        self.con.commit()

    #Store
    def get_books(self, user_hash):
        query = "SELECT book_id, book_title FROM store WHERE user_hash=%s"
        self.cur.execute(query, (user_hash,))
        return self.cur.fetchall()
    
    def add_book(self, user_hash, book_id, book_title):
        query = "INSERT INTO store VALUES (%s, %s, %s)"
        self.cur.execute(query, (user_hash, book_id, book_title))
        self.con.commit()
    
    def is_book(self, user_hash, book_id):
        query = "SELECT book_id FROM store WHERE user_hash=%s AND book_id=%s"
        self.cur.execute(query, (user_hash, book_id))
        res = self.cur.fetchall()
        return len(res) > 0
    
    def delete_book(self, user_hash, book_id):
        query = "DELETE FROM store WHERE user_hash=%s AND book_id=%s"
        self.cur.execute(query, (user_hash, book_id))
        self.con.commit()

    def get_book_title(self, user_hash, book_id):
        query = "SELECT book_title FROM store WHERE user_hash=%s AND book_id=%s"
        self.cur.execute(query, (user_hash, book_id))
        return self.cur.fetchone()[0]

        

    