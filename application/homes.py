from flask import Blueprint, flash, json, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import case, select
from application.extension import db
from application.database.models import Home, Floor, Room
from application.floors import define_floors, set_active_floor
from logs.logging_config import ApplicationLogger

homes = Blueprint('homes', __name__)
logger = ApplicationLogger.get_logger(__name__)

@homes.route('/home/active', methods=['PUT'])
@login_required
def set_active_home(home_id):
    current_user.active_home_id = home_id
    home_query = select(Home).where(Home.id == home_id)
    home = db.session.execute(home_query).scalar_one_or_none()
    if home.user_id == current_user.id:
        current_user.active_home = home
        db.session.commit()
        logger.debug(f'current_user.active_home: {current_user.active_home}')
        return home #the object of the current active home
    
@homes.route('/home/size', methods=['GET','POST'])
@login_required
def home_size():
    if request.method == 'GET':
        return render_template('homes/size_home.html.jinja')
    if request.method == 'POST':
        #500sqft - 3000sqft+
        size_sqft = request.form.get('size') #[ ] change to metric or imperial by user preferences
        logger.debug(f'size_sqft: {size_sqft}')
        size_sqm = int(size_sqft) * 0.092903
        logger.debug(f'size_sqm: {size_sqm}')
        current_user.active_home.home_size_sqm = size_sqm
        db.session.commit()
        return redirect(url_for('homes.home_setup'))

@homes.route('/home/setup', methods=['GET'])
@login_required
def home_setup():
    if not current_user.active_home:
        return render_template('homes/create_home.html.jinja')
    current_home = current_user.active_home
    logger.debug(f'current_home: {current_home} name: {current_home.name}')
    logger.debug(f'current_home.floors.count(): {current_home.floors.count()}')
    if not current_home.active_floor or not current_home.ground_floor:
        return redirect(url_for('floors.define_floors'))
    logger.debug(f'current_home.active_floor: {current_home.active_floor}')
    if not current_home.home_size_sqm:
        logger.debug('home_size_sqm is None')
        return redirect(url_for('homes.home_size'))
    if current_home.floors:
        for floor in current_home.floors: # check if all floors have rooms
            logger.debug(f'floor.rooms.count() {floor} = {floor.rooms.count()}')
            if floor.rooms.count() == 0:
                logger.debug(f'floor {floor.name} has no rooms')
                flash(f'floor {floor.name} has no rooms' , category='danger')
                return redirect(url_for('rooms.define_rooms', floor_id=floor.id))
    return redirect(url_for('map.home_map'))
    
@homes.route('/home/rename', methods=['GET'])
@login_required
def rename_home():
    return render_template('homes/rename_home.html.jinja')