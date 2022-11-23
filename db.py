import sqlite3
import os

class DB:
    def __init__(self):
        if not os.path.isfile("bookstore.db"):
            self.con = sqlite3.connect("bookstore.db")

            self.cur = self.con.cursor()

            self.create_db()

        else:
            self.con = sqlite3.connect("bookstore.db")

            self.cur = self.con.cursor()


    def create_db(self):
        self.cur.execute("CREATE TABLE users(user_hash)")
        self.cur.execute("CREATE TABLE store(user_hash, books_id)")
        self.cur.execute("CREATE TABLE book(id, title, date)")

    def get_users(self):
        query = "SELECT user_hash from users"
        res = self.cur.execute(query)
        
        return res.fetchall()
    
    def add_user(self, user_hash):
        query = "INSERT INTO users VALUES (?)"
        self.cur.execute(query, (user_hash,))
        self.con.commit()        

    def is_user(self, user_hash):
        query = "SELECT user_hash from users WHERE user_hash=?"
        res = self.cur.execute(query, (user_hash,))
        
        return len(res.fetchall()) > 0

    def delete_user(self, user_hash):
        query = "DELETE FROM users WHERE user_hash=?"
        self.cur.execute(query, (user_hash,))
        self.con.commit()

