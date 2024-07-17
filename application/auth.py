#TODO: #21 login and register routes

from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from utils import login_required, apology
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SECRET_KEY'] = secret_key  # Change this to a random secret key

Session(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Log the user in
            session['user_id'] = user.id
            #TODO: #21 Add session management
            return redirect(url_for('/'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
        
        #Old code
'''        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) == 0:
            return apology("invalid username and/or password", 403)
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
        return render_template("login.html")'''


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")
#TODO: #21 Add hashing to password
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")
#TODO: #21 Add hashing to password
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
       
       #OLD CODE 
'''    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        hashed_password = generate_password_hash(password)
        if username == "":
            return apology("invalid username, you left it blank", 400)
        if password == "":
            return apology("invalid password, you left it blank", 400)
        if rows:
            return apology("username is already taken", 400)
        if confirmation != password:
            return apology("passwords do not match", 400)
        if len(rows) != 0:
            return apology("username already exists", 400)
        else:
            try:
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                           username, hashed_password)
            except Exception as e:
                return apology("An error occurred: " + str(e), 400)
        return render_template("login.html")'''


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """reset password"""
    user_id = session["user_id"]
    username_row = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_row[0]['username']
    print(f"username: {username}")
    if request.method == "GET":
        return render_template("password.html", username=username)
    if request.method == "POST":
        # username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        hashed_password = generate_password_hash(password)
        if username == "":
            return apology("invalid username, you left it blank", 403)
        if password == "":
            return apology("invalid password, you left it blank", 403)
        # if rows:
            # return apology("username is already taken", 403)
        if confirmation != password:
            return apology("passwords do not match", 403)
        # if len(rows) != 0:
            # return apology("username already exists", 403)
        else:
            try:
                db.execute('UPDATE users SET hash = ? WHERE ID = ?', hashed_password, user_id)
                # db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
            except Exception as e:
                return apology("An error occurred: " + str(e), 403)
        return logout()
        # return render_template("login.html")
