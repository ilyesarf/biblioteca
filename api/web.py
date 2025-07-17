import os

from flask import Flask, render_template, request, redirect, make_response, url_for

from db import DB
from nanolock_api import NanoLockClient
import utils

if all([os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_USER"), os.getenv("DB_PASS"), os.getenv("DB_NAME")]):
	db = DB(os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_USER"), os.getenv("DB_PASS"), os.getenv("DB_NAME"))
	
app = Flask(__name__)

nanolock = NanoLockClient()

upload_dir = 'upload_dir/'
if not os.path.exists(upload_dir):
	os.mkdir(upload_dir)


#AUTH
@app.route("/signup", methods=["POST"])
def signup():
	app.logger.info(request.json["user_hash"])
	user_hash = request.json.get("user_hash")
	b64enc_img = request.json.get("b64enc_img")
	#app.logger.info(user_hash, b64enc_img)
	if not user_hash or not b64enc_img:
		return {"success": False, "error": "Missing user_hash or image"}, 400
	if db.is_user(user_hash):
		return {"success": False, "error": "User already exists"}, 409
	success, reason = nanolock.add_user(user_hash, b64enc_img)
	if success:
		db.add_user(user_hash)
		return {"success": True, "message": "User created"}, 201
	else:
		return {"success": False, "error": reason}, 400

@app.route("/login", methods=["POST"])
def login():
	user_hash = request.form.get("user_hash")
	b64enc_img = request.form.get("b64enc_img")
	if not user_hash or not b64enc_img:
		return {"success": False, "error": "Missing user_hash or image"}, 400
	if not db.is_user(user_hash):
		return {"success": False, "error": "User doesn't exist"}, 404
	verified, reason = nanolock.verify_face(user_hash, b64enc_img)
	if verified:
		# Optionally set a session cookie here if needed
		return {"success": True, "message": "Login successful"}, 200
	else:
		return {"success": False, "error": reason}, 401

@app.route('/logout', methods=["POST"])
def logout():
	# If you want to handle session cookies, do it here
	return {"success": True, "message": "Logged out"}, 200

@app.route("/delete_user", methods=["POST"])
def delete_user():
	user_hash = request.form.get("user_hash")
	b64enc_img = request.form.get("b64enc_img")
	if not user_hash or not b64enc_img:
		return {"success": False, "error": "Missing user_hash or image"}, 400
	if not db.is_user(user_hash):
		return {"success": False, "error": "User not found!"}, 404
	verified, _ = nanolock.verify_face(user_hash, b64enc_img)
	if verified:
		db.delete_user(user_hash)
		return {"success": True, "message": "User deleted"}, 200
	else:
		return {"success": False, "error": "U can't delete another user's account"}, 401

#STORE
@app.route("/store", methods=["GET"])
def store():
	try:
		user_hash = request.cookies.get("session_id")
		if db.is_user(user_hash):
			books = db.get_books(user_hash)
			return render_template("store/store.html", books=books)
		else:
			return redirect('/')

	except:
		return redirect('/')

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
	error = None

	if request.method == "POST":
		try:
			user_hash = request.cookies.get('session_id')
			if db.is_user(user_hash):
				book = request.files['book']

				book_id = utils.upload_file(user_hash, upload_dir, book)
				book_title = request.form['book_title']

				db.add_book(user_hash, book_id, book_title)

				return redirect('/store')
			else:
				return redirect('/')

		except utils.EXTENSION_NOT_ALLOWED:
			error = "File extension is not allowed"

		except Exception as e:
			error = e

	return render_template('store/add_book.html', error=error)

@app.route("/delete_book", methods=["POST"])
def delete_book():
	user_hash = request.cookies.get('session_id')
	book_id = request.form["book_id"]
	utils.remove_file(user_hash, upload_dir, book_id)

	db.delete_book(user_hash, book_id)

	return redirect('/store')

# READER
@app.route('/reader', methods=['GET', 'POST'])
def reader():
	user_hash = request.cookies.get('session_id')
	user_upload_dir = f"{upload_dir}{user_hash}/"
	book_id = request.args.get('book_id')
	if book_id not in [book[0] for book in db.get_books(user_hash)]: #check if book_id exists
		return redirect('/store')

	book_path = utils.get_file_path(user_upload_dir, book_id)
	book_title = db.get_book_title(user_hash, book_id)

	return render_template('reader.html', book_title=book_title, book_path=f"{user_upload_dir}{book_path}")

	#todo: add check for book path

if __name__ == '__main__':
	app.run(host = "0.0.0.0", port="8000", debug=True)