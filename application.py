import re
import cs50
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import apology, login_required, usd
from news1 import getHeadlines

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = cs50.SQL("sqlite:///corona.db")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/headlines")
@login_required
def headlines():
    headlines = getHeadlines()
    return render_template("headlines.html", headlines=headlines)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            a = "must provide username"
            return render_template("login.html",message=a)

        # Ensure password was submitted
        elif not request.form.get("password"):
            a = "must provide password"
            return render_template("login.html", message=a)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            a = "invalid username and/or password"
            return render_template("login.html", message=a)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    """Register user"""

    if request.method == "POST":

        '''INPUT VALIDATION'''
        # Ensure username was submitted
        if not request.form.get("username"):
            a = "must provide username"
            return render_template("register.html", message=a)

        # Query Database
        elif db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username")):
            a = "username taken"
            return render_template("register.html", message=a)

        # Ensure password was submitted
        elif not request.form.get("password"):
            a = "must provide password"
            return render_template("register.html", message=a)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            a = "must confirm password"
            return render_template("register.html", message=a)

        #check passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            a = "passwords do not match"
            return render_template("register.html", message=a)

        elif re.search('[0-9]',request.form.get("password")) is None:
            a = "Make sure your password has a number in it"
            return render_template("register.html", message=a)

        elif re.search('[A-Z]',request.form.get("password")) is None:
            a = "Make sure your password has a capital letter in it"
            return render_template("register.html", message=a)
        else:
            db.execute("INSERT INTO users (username,hash) VALUES (:uname,:pword)",uname=username,pword=generate_password_hash(password))
            id = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)[0]["id"]
            db.execute("INSERT INTO videos (id) VALUES (:id)",id=id)
            # Redirect user to home page
            return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/info")
@login_required
def info():
    return render_template("info.html")

@app.route("/entertainment", methods=["GET", "POST"])
@login_required
def entertainment():
    if request.method == "POST":
        message = request.form.get("type")
        if message == "video":
            return redirect("/videos")
        else:
            return redirect("/text")
    else:
        return render_template("entertainment.html")

@app.route("/videos", methods=["GET","POST"])
@login_required
def videos():
    if request.method == "GET":
        return render_template("videos.html")
    else:
        for i in range(1,10):
            x = request.form.get(str(i))
            if x != None:
                link = x
                break
        savedVideos = db.execute("SELECT video1, video2, video3, video4, video5 FROM videos WHERE id=:id AND (video1 IS NULL OR video2 IS NULL OR video3 IS NULL OR video4 IS NULL OR video5 IS NULL);",id=session["user_id"])
        if savedVideos == []:
            a = "you have already saved 5 videos"
            return render_template("videos.html", message=a)
        else:
            savedVideos = savedVideos[0]
        for item in savedVideos.keys():
            if savedVideos[item] == link:
                a = "you have already saved this video"
                return render_template("videos.html", message=a)
        for vid in savedVideos.keys():
            if savedVideos[vid] == None:
                db.execute("UPDATE videos SET :column = :link WHERE id=:id",column=vid,link=link, id=session["user_id"])
                return render_template("videos.html")



@app.route("/text")
@login_required
def text():
    return render_template("text.html")

@app.route("/saved_videos", methods=["GET", "POST"])
@login_required
def savedVids():
    if request.method == "POST":
        removeLink = request.form.get("remove")
        links = db.execute("SELECT video1, video2, video3, video4, video5 FROM videos WHERE id=:id", id=session["user_id"])[0]
        for pair in links.items():
            if pair[1] == removeLink:
                column = pair[0]
        db.execute("UPDATE videos SET :column = NULL WHERE id=:id",id=session["user_id"], column=column)
    vidLinks = []
    links = db.execute("SELECT video1, video2, video3, video4, video5 FROM videos WHERE id=:id",id=session["user_id"])[0]
    for item in links:
        if links[item] != None:
            vidLinks.append(links[item])
    if vidLinks == []:
        error = "you have no saved videos"
        return render_template("savedVids.html",error=error)
    return render_template("savedVids.html",vidLinks=vidLinks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



