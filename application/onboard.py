from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from application.extension import db

from logs.logging_config import ApplicationLogger

onboard = Blueprint('onboard', __name__)
logger = ApplicationLogger.get_logger(__name__)

@onboard.route('/tutorial/pingrid', methods=['GET', 'POST'])
@login_required
def pingrid_tutorial():
    if request.method == "POST":
        current_user.tutorial_pingrid_dismissed = True
        db.session.commit()
        return "", 204
    if request.method == "GET":
        return render_template('onboarding/modal/modal_roompingrid.jinja')

@onboard.route('/tutorial/photo', methods=['GET', 'POST'])
@login_required
def photo_tutorial():
    if request.method == "POST":
        current_user.tutorial_photo_dismissed = True
        db.session.commit()
        return "", 204
    if request.method == "GET":
        return render_template('onboarding/modal/modal_photo.jinja')
    
@onboard.route('/tutorial/create_floors', methods=['GET', 'POST'])
@login_required
def floors_tutorial():
    if request.method == "POST":
        current_user.tutorial_floors_dismissed = True
        db.session.commit()
        return "", 204 
    if request.method == "GET":
        return render_template('onboarding/modal/modal_floors.jinja')

@onboard.route('/tutorial/create_rooms', methods=['GET', 'POST'])
@login_required
def rooms_tutorial():
    if request.method == "POST":
        current_user.tutorial_rooms_dismissed = True
        db.session.commit()
        return "", 204
    if request.method == "GET":
        return render_template('onboarding/modal/modal_create_rooms.jinja')
    
@onboard.route('/tutorial/create_home', methods=['GET', 'POST'])
@login_required
def home_tutorial():
    if request.method == "POST":
        current_user.tutorial_home_dismissed = True
        db.session.commit()
        return "", 204
    if request.method == "GET":
        return render_template('onboarding/modal/modal_home.jinja')
    
@onboard.route('/tutorial/map', methods=['GET', 'POST'])
@login_required
def map_tutorial():
    if request.method == "POST":
        current_user.tutorial_map_dismissed = True
        db.session.commit()
        return "", 204
    if request.method == "GET":
        return render_template('onboarding/modal/modal_map.jinja')