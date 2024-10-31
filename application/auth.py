import re
from flask import Blueprint, Flask, flash, make_response, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timezone
from .database.models import User
from .utils import apology

from .extension import db  

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    #session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            flash("must provide username", category="danger")

        elif not password:
            flash("must provide password", category="danger")

        else:
            username_query = select(User).where(User.username == username)
            user = db.session.execute(username_query).scalars().first()
            if user is None:
                flash("Username does not exist", category="danger")
                return '', 400

            elif not check_password_hash(user.password_hash, password):
                flash("Invalid password", category="danger")
                return '', 400
            else:
                login_user(user) 
                flash("Successful login", category="success")
                user.last_login = datetime.now(timezone.utc)
                db.session.commit()
                response = make_response('', 200)
                response.headers['HX-Redirect'] = url_for('main.index')
                return response
    if request.method == "GET":
        return render_template('auth/login.html')

@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    #session.clear()
    logout_user()

    # Redirect user to login form
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        #email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")
        
        username_query = select(User).where(User.username == username)
        #email_query = select(User).where(User.email == email)
        # form validation check
        if not username or not password or not confirmation: #or not email
            flash("All fields are required", category="danger")
        elif password != confirmation:
            flash("Passwords do not match", category="danger")
        elif db.session.execute(username_query).scalars().first():
            flash(f"Username: {username} already exists", category="danger")
        #elif db.session.execute(email_query).scalars().first():
        #    flash(f"Email: {email} already exists", category="danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password) #email=email,
            
            db.session.add(new_user)
            db.session.commit()
            # Log in the new user
            login_user(new_user)
            flash("Account Successfully created", category="success")
            return redirect(url_for('auth.login'))
    
    return render_template("auth/register.html")

@auth.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """reset password"""
    user = current_user
    
    if request.method == "POST":
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not new_password or not confirmation:
            flash("All fields are required", category="danger")
        elif new_password != confirmation:
            flash("Passwords do not match", category="danger")
        else:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            
            logout_user()
            flash("Password successfully changed", category="success")
            return redirect(url_for('auth.login'))
        
    return render_template("auth/password.html", username=user.username)

@auth.route("/validate/<string:item_model>", methods=["POST"])
@login_required
def validate(item_model):
    error_class = ""
    error_message = ""
    name = request.form.get("name_input")
    value = name
    if item_model == "Home":
        placeholder="Home Name"
        id = "HomeName"
        if not name:
            error_class = "is-invalid"
            error_message = f"Home name cannot be empty"
        elif not name[0].isalpha():
            error_class = "is-invalid"
            error_message = "Home name must start with a letter"
        elif not re.search('[a-zA-Z]', name):
            error_class = "is-invalid"
            error_message = f"Home name must contain letters"
        elif len(name) > 80:
            error_class = "is-invalid"
            error_message = f"Home name cannot exceed 80 characters"
            
        elif any(home.name == name for home in current_user.homes):
            error_class = "is-invalid"
            error_message = f"Home name {name} already exists"
        else:
            error_class = "is-valid"
            error_message = ""
    return render_template("homes/validate.html.jinja", error_class=error_class, error_message=error_message, placeholder=placeholder, id=id, item_model=item_model, value=value)