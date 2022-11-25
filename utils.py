
import os

from db import DB
from uuid import uuid4


db = DB()

class EXTENSION_NOT_ALLOWED(Exception):
    pass

def allowed_file(file_extension):
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx'}
    return file_extension in ALLOWED_EXTENSIONS

def upload_file(user_hash, upload_dir, book):
    user_upload_dir = f"{upload_dir}{user_hash}/"
    if not os.path.exists(user_upload_dir):
        os.mkdir(user_upload_dir)

    extension = '.'+book.filename.split('.')[-1].lower()
    if not allowed_file(extension):
        raise EXTENSION_NOT_ALLOWED

    book_id = str(uuid4()).replace('-', '')

    book.save(os.path.join(user_upload_dir, (book_id+extension)))

    return book_id

def get_file_path(user_upload_dir, book_id): 
    for filename in os.listdir(user_upload_dir):
        if os.path.splitext(filename)[0] == book_id:
            return filename
    
    return ''

def remove_file(user_hash, upload_dir, book_id):
    user_upload_dir = f"{upload_dir}{user_hash}/"
    book_path = get_file_path(user_upload_dir, book_id)

    os.remove(f"{user_upload_dir}{book_path}")