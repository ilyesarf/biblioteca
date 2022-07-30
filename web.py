import sys, os, json, shutil
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request
from hashlib import md5
from nanolock.recognizer import Recognizer


app = Flask(__name__)

recognizer = Recognizer()

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
	if request.method == "POST":
		username = request.form["username"]

		if check_user(username) == False:
			recognizer.setup(username)
			return render_template("login.html", username=request.form["username"])
		else:
			return render_template("login.html")

	return render_template('signup.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	usernames= json.loads(open("usernames.json", "r").read())
	error = None
	
	if request.method == "POST":
		username = recognizer.recognize(usernames["usernames"])
		if username != False:
			return render_template("welcome.html", username=username)
		else:
			error = "User not found"

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
			if recognizer.recognize(usernames["usernames"]) == username:

				if len(usernames["usernames"]) == 2 and usernames["usernames"][0] == "Unknown":
					usernames["usernames"].remove(username)
					json.dump(usernames, open("usernames.json", "w"))

					shutil.rmtree(f"nanolock/dataset/{md5(username.encode()).hexdigest()}")
					shutil.rmtree("nanolock/model")

				else:
					usernames["usernames"].remove(username)
					json.dump(usernames, open("usernames.json", "w"))
					recognizer.usernames = usernames

					shutil.rmtree(f"nanolock/dataset/{md5(username.encode()).hexdigest()}")

					shutil.rmtree("nanolock/model")
					os.makedirs("nanolock/model")
					recognizer.train()

				return render_template("index.html")
			else:
				error = "U can't delete another user's account"

		else:
			error = "User not found!"

	return render_template("delete_user.html", error=error)

app.run(host='0.0.0.0', port="8080")