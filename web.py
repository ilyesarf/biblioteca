import sys, os, json
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request, redirect, make_response

from db import DB
from nanolock.recognizer import Verification
from nanolock.recognizer import NoFaceDetected

db = DB()
app = Flask(__name__)

verifier = Verification()

@app.route("/", methods=["GET"])
def index():
	try:
		user_hash = request.cookies.get("session_id")
		if db.is_user(user_hash):
			return redirect('/welcome')
		else:
			return render_template('index.html')
	except:
		return render_template("index.html")

@app.route("/welcome")
def welcome():
	return render_template("welcome.html")

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

	return render_template('signup.html', error=error)


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
					response = make_response(redirect("/welcome"))
					response.set_cookie('session_id', user_hash)

					return response
				else:
					error = f"Face doesnt match !!"

			except NoFaceDetected:
				error = "Face not detected"
		else:
			error = f"User doesn't exist"
	
	return render_template("login.html", error=error)

@app.route('/logout', methods=["GET"])
def logout():
	#delete cookie
	response = make_response(redirect("/"))
	response.delete_cookie('session_id')

	return response

@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
	error = None

	try:
		users = json.loads(open("users.json", "r").read())
	except FileNotFoundError:
		error = "No users in db"
		return render_template("delete_user.html", error=error)
	
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

	return render_template("delete_user.html", error=error)


if __name__ == '__main__':
	app.run(host = "0.0.0.0", port="8080", debug=True)