import logging
from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from application.floors import set_active_floor
from application.rooms import floor_room_check, get_room_list, set_active_room
from logs.logging_config import ApplicationLogger

map = Blueprint('map', __name__)
logger = ApplicationLogger.get_logger(__name__)

@map.route('/map/', methods=['GET'])
@map.route('/map/Floor/<int:floor_id>', methods=['GET'])
@login_required
def home_map(floor_id: int=None):
    view = 'map'
    session['view'] = view
    if floor_id is None:
        if not current_user.active_home:
            return redirect(url_for('homes.home_setup'))
        floor_id = current_user.active_home.active_floor_id
        if floor_id is None:
            return redirect(url_for('floors.define_floors'))
    logger.debug(f'map called with floor_id: {floor_id}')
    # goes to map view of current active floor
    floor_id, has_rooms = floor_room_check(floor_id)
    logger.debug(f'room check: floor_id: {floor_id}, has_rooms: {has_rooms}')
    floor = set_active_floor(floor_id)
    if has_rooms is False:
        logger.debug(f'Floor {floor.name} has no rooms, please add some')
        flash(f'Floor {floor.name} has no rooms, please add some' , category='danger')
        return redirect(url_for('rooms.define_rooms', floor_id=floor_id))
    floor_list, room_list = get_room_list()
    logger.debug(f'floor_list MAP: {floor_list}')
    return render_template('map/index.html.jinja', view=view)
    raise NotImplementedError("map not yet implemented")

@map.route('/map/Room/<int:room_id>', methods=['GET'])
@login_required
def room_redirect(room_id: int):
    set_active_room(room_id)
    return render_template('walkthrough/index.html.jinja')