import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import datetime
import re

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Query the transactions table to get symbol, sum of shares, and price for the user
    transaction_query = "SELECT symbol, SUM(shares) AS total_shares, price FROM transactions WHERE user_id = ? AND symbol NOT IN ('None', 'Fund', 'Fund added') GROUP BY symbol;"
    transaction_db = db.execute(transaction_query, user_id)

    # Query the users table to get the user's available cash
    cash_query = "SELECT cash FROM users WHERE id = ?"
    cash_db = db.execute(cash_query, user_id)
    cash = cash_db[0]["cash"]

    return render_template("index.html", transactions=transaction_db, cash=cash)


from flask import Flask, render_template, request, redirect, session, flash
import datetime

# Assuming you have already defined the Flask app and configured it

from flask import Flask, render_template, request, redirect, session, flash
import datetime
import re  # Import regular expression module

# Assuming you have already defined the Flask app and configured it


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        shares_str = request.form.get("shares")

        # Check if symbol is provided
        if not symbol:
            return apology("Must give symbol")

        stock = lookup(symbol.upper())

        # Check if the symbol exists
        if stock is None:
            return apology("Symbol does not exist")

        # Check if shares input is numerical and non-negative
        if not re.match(r"^\d+$", shares_str):
            return apology("Shares should be a non-negative whole number")

        shares = int(shares_str)
        if shares <= 0:
            return apology("Shares should be more than zero")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]

        # Retrieve user's cash from the database
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        # Check if the user has enough money
        if user_cash < transaction_value:
            return apology("Not enough money")

        update_cash = user_cash - transaction_value

        # Update user's cash in the database
        db.execute(
            "UPDATE users SET cash = :update_cash WHERE id = :user_id",
            update_cash=update_cash,
            user_id=user_id,
        )

        date = datetime.datetime.now()

        # Insert a new transaction record into the database
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            shares,
            stock["price"],
            date,
        )

        flash("Bought!")

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0",
            id=user_id,
        )

        symbols_list = [row["symbol"] for row in symbols_user]
        return render_template("sell.html", symbols=symbols_list)
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Must provide a symbol")

        stock = lookup(symbol.upper())

        if stock is None:
            return apology("Symbol does not exist")

        if shares <= 0:
            return apology("Shares should be more than zero")

        user_id = session["user_id"]

        user_shares_row = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id= :id AND symbol= :symbol GROUP BY symbol",
            id=user_id,
            symbol=symbol,
        )
        user_shares_real = user_shares_row[0]["total_shares"]

        if shares > user_shares_real:
            return apology("You do not have this amount of shares")

        user_cash_row = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_row[0]["cash"]

        transaction_value = shares * stock["price"]
        update_cash = user_cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        date = datetime.datetime.now()

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            -shares,
            stock["price"],
            date,
        )

        flash("Sold!")

        return redirect("/")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    tranctions_db = db.execute(
        "SELECT * FROM transactions WHERE user_id = :id", id=user_id
    )
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
    cash = cash[0]["cash"]

    return render_template("history.html", tranctions=tranctions_db, cash=cash)


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    """Add cash to the user's account"""
    if request.method == "GET":
        return render_template("addCash.html")
    else:
        added_cash_str = request.form.get("added_cash")

        # Check if added_cash input is numerical and positive
        try:
            added_cash = float(added_cash_str)
            if added_cash <= 0:
                return apology("Added cash should be positive")
        except ValueError:
            return apology("Invalid input for added cash")

        user_id = session["user_id"]

        # Retrieve user's current cash from the database
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        cash = user_cash_db[0]["cash"]

        new_cash = cash + added_cash
        date = datetime.datetime.now()

        # Update user's cash in the database
        db.execute(
            "UPDATE users SET cash = :new_cash WHERE id = :user_id",
            new_cash=new_cash,
            user_id=user_id,
        )

        # Insert a new transaction record for the fund addition
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)",
            user_id,
            "Fund added",
            "Fund added",
            added_cash,
            date,
        )

        flash("Success")

        return render_template("addCash.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must Give Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does not exist")

        return render_template(
            "quoted.html",
            name=stock["name"],
            price=stock["price"],
            symbol=stock["symbol"],
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # forget any user_id
    # session.clear()
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username shouldn't be empaty")
        if not password:
            return apology("Password shouldn't be empaty")
        if not confirmation:
            return apology("confirm password shouldn't be empaty")
        if password != confirmation:
            return apology("Password do not match!")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
        except:
            return apology("Username already exists")

        session["user_id"] = new_user
        return redirect("/")

