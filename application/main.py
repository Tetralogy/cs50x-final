from datetime import datetime
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import time
from application.database.models import Home, Room, Task, User, UserStatus
from .utils import handle_error, apology
from .extension import db
from .database.schemas import task_schema, user_schema  # Import other schemas as needed

main = Blueprint('main', __name__)

# Register the error handler
main.errorhandler(Exception)(handle_error)

# Define a context processor to make current_user available in every template
'''@main.context_processor
@login_required
def inject_current_user():
    onboarded = Home.query.filter_by(user_id=current_user.id).first() is not None
    return dict(current_user=current_user, onboarded=onboarded)'''

@main.route('/')
@login_required
def index():
    print('index called')
    home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    if home_id is not None:
        return render_template('showtasks.html', user=current_user, page=1) #TODO: create user home page/dashboard
    
    return render_template('setup/onboarding.html', user=current_user, onboarded=False)#TODO: complete onboarding loop

@main.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    '''home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    
    if current_user.profile_picture_url is None:
    if currentuser has no home id
    if current_user has no room id
    if current_user has no tasks
    if current_user has no status'''
    """ raise NotImplementedError("onboarding not yet implemented") """


@main.route('/walkthrough', methods=['GET', 'POST'])
@login_required
def walkthrough():
    raise NotImplementedError("walkthrough not yet implemented")



@main.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    raise NotImplementedError("map not yet implemented")

@main.route('/tasklist', methods=['GET', 'POST'])
@login_required
def tasklist():
    raise NotImplementedError("tasklist not yet implemented")