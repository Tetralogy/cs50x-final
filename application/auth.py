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
