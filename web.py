import sys, os, json, shutil
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request
from hashlib import md5
from nanolock.recognizer import Verification
from nanolock.recognizer import NoFaceDetected


app = Flask(__name__)

verifier = Verification()

def check_user(username):
	if os.path.isfile("usernames.json"):
		with open("usernames.json", "r") as f:
			usernames = json.loads(f.read())
			if username in usernames["usernames"]:
				return True

	return False

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	error = None

	if request.method == "POST":
		username = request.form["username"]

		if check_user(username) == False:
			try:
				verifier.setup(username)
				return render_template("login.html")
			except NoFaceDetected:
				error="No Face Was Detected"
				
				verifier.usernames["usernames"].remove(username)
				json.dump(verifier.usernames, open("usernames.json", "w"))

				shutil.rmtree(f"nanolock/dataset/{md5(username.encode()).hexdigest()}")

		else:
			return render_template("login.html")

	return render_template('signup.html', error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	
	if request.method == "POST":
		username = request.form["username"]

		accept_login = False
		try:
			accept_login = verifier.accept_login(username)

			if accept_login:
				return render_template("welcome.html", username=username)
			else:
				error = f"You are not {username} !!"

		except NoFaceDetected:
			error = "Face not detected"

	return render_template("login.html", error=error)

@app.route("/delete_user", methods=["GET", "POST"])
def delete_user():
	usernames = json.loads(open("usernames.json", "r").read())

	error = None

	if request.method == "POST":
		username = request.form["username"]
		if username == "Unknown":
			error = "You cannot delete 'Unknown' user"

		if check_user(username):
			if verifier.accept_login(username):

				if len(usernames["usernames"]) == 2 and usernames["usernames"][0] == "Unknown":
					usernames["usernames"].remove(username)
					json.dump(usernames, open("usernames.json", "w"))

					shutil.rmtree(f"nanolock/dataset/{md5(username.encode()).hexdigest()}")

				else:
					usernames["usernames"].remove(username)
					json.dump(usernames, open("usernames.json", "w"))
					verifier.usernames = usernames

					shutil.rmtree(f"nanolock/dataset/{md5(username.encode()).hexdigest()}")

				return render_template("index.html")
			else:
				error = "U can't delete another user's account"

		else:
			error = "User not found!"

	return render_template("delete_user.html", error=error)

app.run(host='0.0.0.0', port="8080")