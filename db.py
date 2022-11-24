import sqlite3
import os

class DB:
    def __init__(self):
        if not os.path.isfile("bookstore.db"):
            self.con = sqlite3.connect("bookstore.db", check_same_thread=False)

            self.cur = self.con.cursor()

            self.create_db()

        else:
            self.con = sqlite3.connect("bookstore.db", check_same_thread=False)

            self.cur = self.con.cursor()

    def create_db(self):
        self.cur.execute("CREATE TABLE users(user_hash)")
        self.cur.execute("CREATE TABLE store(user_hash, book_id, book_title, book_date)")

    #Users
    def get_users(self):
        query = "SELECT user_hash FROM users"
        res = self.cur.execute(query)
        
        return res.fetchall()
    
    def add_user(self, user_hash):
        query = "INSERT INTO users VALUES (?)"
        self.cur.execute(query, (user_hash,))
        self.con.commit()        

    def is_user(self, user_hash):
        query = "SELECT user_hash FROM users WHERE user_hash=?"
        res = self.cur.execute(query, (user_hash,))
        
        return len(res.fetchall()) > 0

    def delete_user(self, user_hash):
        query = "DELETE FROM users WHERE user_hash=?"
        self.cur.execute(query, (user_hash,))
        self.con.commit()

    #Store
    def get_books(self, user_hash):
        query = "SELECT book_id, book_title, book_date FROM store WHERE user_hash=?"
        res = self.cur.execute(query, (user_hash,))

        return res.fetchall()
    
    def add_book(self, user_hash, book_id, book_title, book_date):
        query = "INSERT INTO store VALUES (?, ?, ?, ?)"
        self.cur.execute(query, (user_hash, book_id, book_title, book_date))
        self.con.commit()
    
    def is_book(self, user_hash, book_id):
        query = "SELECT book_id FROM store WHERE user_hash=? AND book_id=?"
        res = self.cur.execute(query, (user_hash, book_id))

        return len(res.fetchall()) > 0
    
    def delete_book(self, user_hash, book_id):
        query = "DELETE FROM store WHERE user_hash=? AND book_id=?"
        self.cur.execute(query, (user_hash, book_id))
        self.con.commit()

    