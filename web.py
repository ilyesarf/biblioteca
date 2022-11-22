import sys, os, json
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request, redirect

from nanolock.recognizer import Verification
from nanolock.recognizer import NoFaceDetected


app = Flask(__name__)

verifier = Verification()

def check_user(user_hash):
	if os.path.isfile("users.json"):
		with open("users.json", "r") as f:
			user_hashes = json.loads(f.read())["user_hashes"]
			if user_hash in user_hashes:
				return True

	return False

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	error = None

	if request.method == "POST":
		user_hash = request.form["user_hash"]
		b64enc_img = request.form["b64enc_img"]

		if check_user(user_hash) == False:
			try:
				verifier.add_user(user_hash, b64enc_img)

				return redirect("/login")
			except NoFaceDetected:
				error="No Face Was Detected"
				
				verifier.users["user_hashes"].remove(user_hash)
				json.dump(verifier.users, open("users.json", "w"))

				os.remove(f"{verifier.dataset_path}{user_hash}.jpg")

		else:
			return redirect("/login")

	return render_template('signup.html', error=error)


@app.route("/login", methods=["GET", "POST"])
def login():

	error = None
	
	if request.method == "POST":
		user_hash = request.form["user_hash"]
		b64enc_img = request.form["b64enc_img"]

		if check_user(user_hash):
			accept_login = False
			
			try:
				accept_login = verifier.accept_login(user_hash, b64enc_img)

				if accept_login:
					return render_template("welcome.html")
				else:
					error = f"Face doesnt match !!"

			except NoFaceDetected:
				error = "Face not detected"
		else:
			error = f"User doesn't exist"
	
	return render_template("login.html", error=error)

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
		
		if check_user(user_hash):
			if verifier.accept_login(user_hash, b64enc_img):

				if len(users["user_hashes"]) == 1:
					users["user_hashes"].remove(user_hash)
					json.dump(users, open("users.json", "w"))

					os.remove(f"nanolock/dataset/{user_hash}.jpg")

				else:
					users["user_hashes"].remove(user_hash)
					json.dump(users, open("users.json", "w"))
					verifier.users = users

					os.remove(f"nanolock/dataset/{user_hash}.jpg")

				return render_template("index.html")
			else:
				error = "U can't delete another user's account"

		else:
			error = "User not found!"

	return render_template("delete_user.html", error=error)

if __name__ == '__main__':
	app.run(host = "0.0.0.0", port="8080", ssl_context='adhoc', debug=True)