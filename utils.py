
import os

from db import DB
from uuid import uuid4
from datetime import date

db = DB()

def upload_file(upload_dir, book):
    extension = book.filename.split('.')[-1].lower()
    book_id = str(uuid4()).replace('-', '')

    book.save(os.path.join(upload_dir, (book_id+extension)))

    return book_id

def remove_file(user_hash, book_id):
    #book_path = 0

    db.delete_book()