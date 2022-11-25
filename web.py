import sys
sys.path.insert(1, 'nanolock/')
import os

from flask import Flask, render_template, request, redirect, make_response

from db import DB
from nanolock.recognizer import Verification
from nanolock.recognizer import NoFaceDetected
import utils

db = DB()
app = Flask(__name__)

verifier = Verification()

upload_dir = 'upload_dir/'
if not os.path.exists(upload_dir):
	os.mkdir(upload_dir)

@app.route("/", methods=["GET"])
def index():
	try:
		user_hash = request.cookies.get("session_id")
		if db.is_user(user_hash):
			return redirect('/store')
		else:
			return render_template('index.html')
	except:
		return render_template("index.html")

#AUTH
@app.route("/signup", methods=["GET", "POST"])
def signup():
	error = None

	if request.method == "POST":
		user_hash = request.form["user_hash"]
		b64enc_img = request.form["b64enc_img"]

		if db.is_user(user_hash) == False:
			try:
				verifier.add_face(user_hash, b64enc_img)
				db.add_user(user_hash)

				return redirect("/login")
			except NoFaceDetected:
				error="No Face Was Detected"

		else:
			return redirect("/login")

	return render_template('auth/signup.html', error=error)

@app.route("/login", methods=["GET", "POST"])
def login():

	error = None
	
	if request.method == "POST":
		user_hash = request.form["user_hash"]
		b64enc_img = request.form["b64enc_img"]

		if db.is_user(user_hash):
			accept_login = False
			
			try:
				accept_login = verifier.accept_login(user_hash, b64enc_img)

				if accept_login:
					#set cookie
					response = make_response(redirect("/store"))
					response.set_cookie('session_id', user_hash)

					return response
				else:
					error = "Face doesnt match !!"

			except NoFaceDetected:
				error = "Face not detected"
		else:
			error = "User doesn't exist"
	
	return render_template("auth/login.html", error=error)

@app.route('/logout', methods=["GET"])
def logout():
	#delete cookie
	response = make_response(redirect("/"))
	response.delete_cookie('session_id')

	return response

@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
	error = None
	
	if request.method == "POST":
		user_hash = request.form["user_hash"]
		b64enc_img = request.form["b64enc_img"]
		
		if db.is_user(user_hash):
			if verifier.accept_login(user_hash, b64enc_img):

				db.delete_user(user_hash)

				#delete cookie
				response = make_response(redirect("/"))
				response.delete_cookie('session_id')
				
				return response
			else:
				error = "U can't delete another user's account"

		else:
			error = "User not found!"

	return render_template("auth/delete_user.html", error=error)

#STORE
@app.route("/store", methods=["GET"])
def store():
	try:
		user_hash = request.cookies.get("session_id")
		if db.is_user(user_hash):
			books = db.get_books(user_hash)
			print(books)
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

if __name__ == '__main__':
	app.run(host = "0.0.0.0", port="8080", debug=True)