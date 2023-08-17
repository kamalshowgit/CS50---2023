import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add the user's entry into the database - retrieve form data
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        id = request.form.get("id")

        if not id:
            # Add birthday to the database
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        else:
            # id is passed so this is an update
            db.execute("UPDATE birthdays SET month = ?, day = ? WHERE id = ?", month, day, id)

        return redirect("/")

    else:
        # GET
        # Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays ORDER BY id")

        return render_template("index.html", birthdays=birthdays)

@app.route("/removerecord", methods=["POST"])
def removerecord():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")


@app.route("/editrecord", methods=["POST"])
def editrecord():

    # Forget registrant
    id = request.form.get("id")
    if id:
        birthdays = db.execute("SELECT * FROM birthdays WHERE id = ?", id)
    return render_template("/editrecord.html", birthdays=birthdays)