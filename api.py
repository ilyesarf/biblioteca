import sys, os, json
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request
from nanolock.recognizer import Recognizer


app = Flask(__name__)

recognizer = Recognizer()

def check_user(username):
	if os.path.isfile("usernames.json"):
		with open("usernames.json", "r") as f:
			usernames = json.loads(f.read())["usernames"]
			if username in usernames:
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
			return render_template("welcome.html", username=request.form["username"])

	return render_template('signup.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	usernames = json.loads(open("usernames.json", "r").read())["usernames"]
	error = None
	
	if request.method == "POST":
		username = recognizer.recognize(usernames)
		if username != False:
			return render_template("welcome.html", username=username)
		else:
			error = "User not found"

	return render_template("login.html", error=error)
	

app.run()