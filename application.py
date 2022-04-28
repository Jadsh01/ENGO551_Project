import os
import requests
from urllib import request


from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine, true
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registration", methods=["POST"])
def registration():
    username=request.form.get("username")
    password=request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).rowcount==1:
        return render_template("error.html", message="Username is already taken.")
    db.execute("INSERT INTO users (username, passwrd) VALUES (:username, :passwrd)", {"username":username, "passwrd":password})
    db.commit()
    return render_template("success.html")

@app.route("/loginform")
def loginform():
    return render_template('loginform.html')

@app.route("/login", methods=["POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username=:username AND passwrd=:password" , {"username":username, "password":password}).rowcount==0:
        return render_template("error.html", message="Account does not exist.")

    user=db.execute("SELECT * FROM users WHERE username=:username AND passwrd=:password" , {"username":username, "password":password}).fetchone()

    session["userid"]=user["userid"]
    session["logged_in"]=True

    return render_template("index.html")