from flask import Blueprint, Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
            user = User.query.filter_by(username=username).first()
            if user is None:
                flash("Username does not exist", category="danger")
            elif not check_password_hash(user.password_hash, password):
                flash("Invalid password", category="danger")
            else:
                login_user(user) 
                flash("Successful login", category="success")
                return redirect(url_for('main.index'))
    return render_template('login.html')

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
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get("confirmation")
        
        # form validation check
        if not username or not email or not password or not confirmation:
            flash("All fields are required", category="danger")
        elif password != confirmation:
            flash("Passwords do not match", category="danger")
        elif User.query.filter_by(username=username).first():
            flash(f"Username: {username} already exists", category="danger")
        elif User.query.filter_by(email=email).first():
            flash(f"Email: {email} already exists", category="danger")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_password)
            
            db.session.add(new_user)
            db.session.commit()
            # Log in the new user
            login_user(new_user)
            flash("Account Successfully created", category="success")
            return redirect(url_for('main.index'))
    
    return render_template("register.html")

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
        
    return render_template("password.html", username=user.username)
