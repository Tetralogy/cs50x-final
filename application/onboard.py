import logging
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from application.extension import db

from application.database.models import Floor, Home, Room
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

'''@onboard.route('/onboarding', methods=['GET'])
@login_required
def onboarding():
    logger.debug('onboarding called')
    if current_user.profile_picture_url is None:
        logger.debug('profile_picture_url is None')
        return render_template('profile/parts/upload_profile_photo.html.jinja')
    home_ids = [home.home_id for home in current_user.homes]
    logger.debug(f'homes: {home_ids}')
    if not home_ids:
        logger.debug('homes is empty')
        return render_template('onboarding/parts/home/index.html.jinja')
    logger.debug(f'current_user.active_home: {current_user.active_home}')
    logger.debug(f'current_user.active_home.active_floor: {current_user.active_home.active_floor}')
    logger.debug(f'current_user.active_home.rooms: {all([floor.rooms for floor in current_user.active_home.floors])}')
    if current_user.active_home and current_user.active_home.active_floor and all([floor.rooms for floor in current_user.active_home.floors]):
        logger.debug('all home, floor, and room are set')
        return render_template('walkthrough/index.html.jinja') #go to walkthrough
    return render_template('onboarding/parts/home/index.html.jinja') #temporary, go to home setup
    
    get the current home id when it is created
    room_ids = [room.room_id for room in current_user.room_ids]
    if not room_ids:
        logger.debug('rooms is empty')
        return render_template('onboarding/parts/room/index.html.jinja')'''
    

        
'''home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    
    if currentuser has no home id
    if current_user has no room id
    if current_user has no tasks
    if current_user has no status
    raise NotImplementedError("onboarding not yet implemented")
    
    
@onboard.route('/start', methods=['GET'])
@login_required
def start():
    return render_template('onboarding/index.html.jinja')

@onboard.route('/onboarding/progress', methods=['GET'])
@login_required
def progress():
    profile_picture_completed = current_user.profile_picture_url is not None
    home_completed = current_user.homes.count() > 0
    floor_completed = current_user.active_home and bool(current_user.active_home.active_floor)
    room_completed = current_user.active_home and any([bool(floor.rooms) for floor in current_user.active_home.floors])
    walkthrough_completed = bool(current_user.active_home and current_user.active_home.last_full_walkthrough)
    
    steps = [
        {'name': 'profile picture', 'completed': profile_picture_completed},
        {'name': 'home', 'completed': home_completed},
        {'name': 'floor', 'completed': floor_completed},
        {'name': 'room', 'completed': room_completed},
        {'name': 'walkthrough', 'completed': walkthrough_completed},
    ]
    progress = int(sum([step['completed'] for step in steps]) / len(steps) * 100)
    
    return render_template('onboarding/parts/progress.html.jinja', progress=progress, steps=steps)


@onboard.route('/onboarding/progress', methods=['PATCH'])
@login_required
def progress_update():
    step = request.args.get('step')
    if step == 'profile_picture':
        current_user.profile_picture_url = request.form['profile_picture_url']
    elif step == 'home':
        current_user.active_home = Home.query.get(request.form['home_id'])
    elif step == 'floor':
        current_user.active_home.active_floor = Floor.query.get(request.form['floor_id'])
    elif step == 'room':
        floor = Floor.query.get(request.form['floor_id'])
        floor.rooms = [Room.query.get(room_id) for room_id in request.form.getlist('room_ids')]
    elif step == 'walkthrough':
        current_user.active_home.walkthrough_completed = True
    else:
        return jsonify(message='Invalid step'), 400
    
    db.session.commit()
    return '', 204
    [ ] clean up unused routes when done and tested'''