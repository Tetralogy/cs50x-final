import logging
import os
from flask import Blueprint, current_app, make_response, redirect, render_template, request, session, url_for
from jinja2.exceptions import TemplateNotFound
from jinja2.exceptions import TemplateError
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db
from application.database.models import Room
from application.floors import set_active_floor
from application.list_utils import get_list_entries_for_item, get_userlist
from application.rooms import set_active_room
from logs.logging_config import ApplicationLogger

walkthrough = Blueprint('walkthrough', __name__)
logger = ApplicationLogger.get_logger(__name__)

@walkthrough.route('/walkthrough/setup', methods=['GET'])
@login_required
def walkthrough_setup():
    floor_list = get_userlist('Floor', f'{current_user.active_home.name} Floors').entries
    return render_template('map/index.html.jinja', floor_list=floor_list)

@walkthrough.route('/walkthrough/', methods=['GET'])
@walkthrough.route('/walkthrough/<int:room_id>', methods=['GET'])
@walkthrough.route('/walkthrough/<room_name>/', methods=['GET'])
@walkthrough.route('/walkthrough/<room_name>/<view>', methods=['GET'])
@walkthrough.route('/walkthrough/start', methods=['GET', 'POST'])
@login_required
def walk_start(room_id: int = None, room_name: str = None, view: str = None):
    if room_id:
        set_active_room(room_id)
    if request.method == 'GET':
        logger.debug(f'get room_name: {room_name}')
        logger.debug(f'get view: {view}')
        if room_name:
            room = db.session.execute(select(Room).where(Room.home_id == current_user.active_home_id).where(Room.name == room_name)).first()
            if room:
                logger.debug(f'room: {room} room_name: {room_name} room name name: {room[0].name}')
                room_id = room[0].id
                set_active_room(room_id)
                if not view:
                    view = 'room'
    if request.method == 'POST':
        logger.debug(f'post room_name: {room_name}')
        logger.debug(f'post view: {view}')
        active_room_id = request.form.get('active_room')
        set_active_room(active_room_id)
        logger.debug(f'active_room: {current_user.active_home.active_room}')
        view = "room"
    session['view'] = view
    logger.debug(f'view: {view}')
    #logger.debug(f'active_room: {active_room}')
    return redirect(url_for('walkthrough.views', view=view))
    #return render_template('walkthrough/index.html.jinja', active_room=active_room)


@walkthrough.route('/walkthrough/steps', methods=['GET', 'PUT'])
@login_required
def views():
    if request.method == 'GET':
        view = request.args.get('view')
        if not view:
            view = session.get('view')

    if request.method == 'PUT':
        view = request.form.get('view')
        logger.debug(f'view: {view}')
        session['view'] = view
    logger.debug(f'view?: {view}')
    
    if os.path.exists(os.path.join(current_app.root_path, 'templates', f'walkthrough/parts/{view}.html.jinja')):
        logger.debug(f'File exists!: walkthrough/parts/{view}.html.jinja')
        
    else:
        logger.debug(f'File not found! {view}.html.jinja')
        view = 'room'

    if 'HX-Request' in request.headers:
        #return render_template(f'walkthrough/parts/{view}.html.jinja', view=view)
        response = make_response(render_template(f'walkthrough/parts/{view}.html.jinja', view=view))
        response.headers['HX-Push'] = f'/walkthrough/{current_user.active_home.active_room.name}/{view}'
        return response
    else:
        #return render_template('walkthrough/index.html.jinja')
        response = make_response(render_template('walkthrough/index.html.jinja', view=view))
        response.headers['HX-Push'] = f'/walkthrough/{current_user.active_home.active_room.name}/{view}'
        return response
    
    

@walkthrough.route('/walkthrough/<string:direction>', methods=['GET'])
@login_required
def walk_next(direction): #todo: get list of all rooms in order by floor
    """ if direction == 'nextfloor':
        direcint = +1
    elif direction == 'prevfloor':
        direcint = -1
        
        home_entry_id = get_list_entries_for_item(current_user.active_home)[0].id
        floors_list = get_userlist('Floor', parent_entry_id=home_entry_id)
        floors_list_ordered = sorted(floors_list.entries, key=lambda x: x.order)
        if not floors_list_ordered:
            # handle the case where the list is empty
            raise Exception('No floors in the list')
        current_active_floor_list_entry = get_list_entries_for_item(current_user.active_home.active_floor)[0]
        for i, floor in enumerate(floors_list_ordered):
            if floor == current_active_floor_list_entry:
                next_floor_index = (i + direcint) % len(floors_list_ordered)
                next_floor = floors_list_ordered[next_floor_index]
                logger.debug(f'next_floor: {next_floor}')
                set_active_floor(next_floor.item_id)
                break """
    if direction == 'next' or direction == 'nextroom':
        direcint = +1
    elif direction == 'prev' or direction == 'prevroom':
        direcint = -1
    else:
        raise ValueError(f'Invalid direction: {direction}')  # Handle unexpected direction values
    current_active_room_list_entry = get_list_entries_for_item(current_user.active_home.active_room)[0]
    if not current_user.active_home.active_room:  
        return 'No active room', 400
    parent_entry_id = get_list_entries_for_item(current_user.active_home.active_floor)[0].id
    #current_user.active_home.active_room_id
    rooms_list = get_userlist(item_model='Room', parent_entry_id=parent_entry_id)
    logger.debug(f'rooms_list: {rooms_list} entries: {rooms_list.entries}') 
    #rooms_list_ordered = iter(sorted(rooms_list.entries, key=lambda x: x.order))
    #logger.debug(f'rooms_list_ordered 1: {rooms_list_ordered}')
    rooms_list_ordered = sorted(rooms_list.entries, key=lambda x: x.order)
    logger.debug(f'rooms_list_ordered 2: {rooms_list_ordered}')
    if not rooms_list_ordered:
        # handle the case where the list is empty
        raise Exception('No rooms in the list')
    for i, room in enumerate(rooms_list_ordered):
        if room == current_active_room_list_entry:
            next_room_index = (i + direcint) % len(rooms_list_ordered)
            next_room = rooms_list_ordered[next_room_index]
            logger.debug(f'next_room: {next_room}')
            set_active_room(next_room.item_id)
            break
    view = 'rename'
    session['view'] = view
    return redirect(url_for('walkthrough.views'))
    #return render_template('walkthrough/index.html.jinja')


#------------------------------------------------------------------------------------------------------------

"""
Pseudo code for walkthrough
1. User starts walkthrough
2. User is asked to confirm the name and type of the room they are in
3. User is asked to upload a panorama picture of the room
4. User is asked to quickly add task drafts for the room
5. User is asked to add photos of areas in the room that contain tasks
6. User is asked to move to the next room
"""

