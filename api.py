import sys
sys.path.insert(1, 'nanolock/')

from flask import Flask, render_template, request
from nanolock.recognizer import Recognizer

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
	username = request.form["username"]
	Recognizer(username).setup()
	return "Done!"

app.run()