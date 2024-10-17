import os
from flask import Blueprint, current_app, make_response, redirect, render_template, request, session, url_for
from jinja2.exceptions import TemplateNotFound
from jinja2.exceptions import TemplateError
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db
from application.database.models import Room
from application.lists import get_list_entries_for_item, get_userlist
from application.rooms import set_active_room

walkthrough = Blueprint('walkthrough', __name__)

@walkthrough.route('/walkthrough/setup', methods=['GET'])
@login_required
def walkthrough_setup():
    walk_setup = True
    session['walk_setup'] = walk_setup
    floor_list = get_userlist('Floor', f'{current_user.active_home.name} Floors').entries
    return render_template('map/index.html.jinja', floor_list=floor_list, walk_setup=walk_setup)

@walkthrough.route('/walkthrough/', methods=['GET'])
@walkthrough.route('/walkthrough/<room_name>/', methods=['GET'])
@walkthrough.route('/walkthrough/<room_name>/<walk_step>', methods=['GET'])
@walkthrough.route('/walkthrough/start', methods=['GET', 'POST'])
@login_required
def walk_start(room_name: str = None, walk_step: str = None):
    if request.method == 'GET':
        print(f'get room_name: {room_name}')
        print(f'get walk_step: {walk_step}')
        if room_name:
            room = db.session.execute(select(Room).where(Room.home_id == current_user.active_home_id).where(Room.name == room_name)).first()
            if room:
                print(f'room: {room} room_name: {room_name} room name name: {room[0].name}')
                room_id = room[0].id
                active_room = set_active_room(room_id)
                if not walk_step:
                    walk_step = 'rename'
                
        
    if request.method == 'POST':
        print(f'post room_name: {room_name}')
        print(f'post walk_step: {walk_step}')
        active_room_id = request.form.get('active_room')
        active_room = set_active_room(active_room_id)
        print(f'active_room: {active_room}')
        walk_step = "rename"
    session['walk_step'] = walk_step
    print(f'walk_step: {walk_step}')
    #print(f'active_room: {active_room}')
    return redirect(url_for('walkthrough.walk_steps', walk_step=walk_step))
    #return render_template('walkthrough/index.html.jinja', active_room=active_room)


@walkthrough.route('/walkthrough/steps', methods=['GET', 'PUT'])
@login_required
def walk_steps():
    if request.method == 'GET':
        walk_step = request.args.get('walk_step')
        if not walk_step:
            walk_step = session.get('walk_step')

    if request.method == 'PUT':
        walk_step = request.form.get('walk_step')
        print(f'walk_step: {walk_step}')
        session['walk_step'] = walk_step
    print(f'walk_step?: {walk_step}')
    
    if os.path.exists(os.path.join(current_app.root_path, 'templates', f'walkthrough/parts/{walk_step}.html.jinja')):
        print(f'File exists!: walkthrough/parts/{walk_step}.html.jinja')
        
    else:
        print(f'File not found! {walk_step}.html.jinja')
        walk_step = 'rename'

    if 'HX-Request' in request.headers:
        #return render_template(f'walkthrough/parts/{walk_step}.html.jinja', walk_step=walk_step)
        response = make_response(render_template(f'walkthrough/parts/{walk_step}.html.jinja'))
        response.headers['HX-Push'] = f'/walkthrough/{current_user.active_home.active_room.name}/{walk_step}'
        return response
    else:
        #return render_template('walkthrough/index.html.jinja')
        response = make_response(render_template('walkthrough/index.html.jinja'))
        response.headers['HX-Push'] = f'/walkthrough/{current_user.active_home.active_room.name}/{walk_step}'
        return response
    
    

@walkthrough.route('/walkthrough/nextroom', methods=['GET'])
@login_required
def walk_next():
    current_active_room_list_entry = get_list_entries_for_item(current_user.active_home.active_room)[0]
    if not current_user.active_home.active_room:  
        return 'No active room', 400
    parent_entry_item_id = current_user.active_home.active_floor_id
    #current_user.active_home.active_room_id
    rooms_list = get_userlist('Room', f'{current_user.active_home.name} {current_user.active_home.active_floor.name} Rooms', parent_entry_item_id)
    print(f'rooms_list: {rooms_list} entries: {rooms_list.entries}')
    rooms_list_ordered = iter(sorted(rooms_list.entries, key=lambda x: x.order))
    print(f'rooms_list_ordered: {rooms_list_ordered}')
    rooms_list_ordered = sorted(rooms_list.entries, key=lambda x: x.order)
    if not rooms_list_ordered:
        # handle the case where the list is empty
        raise Exception('No rooms in the list')
    for i, room in enumerate(rooms_list_ordered):
        if room == current_active_room_list_entry:
            next_room_index = (i + 1) % len(rooms_list_ordered)
            next_room = rooms_list_ordered[next_room_index]
            active_room = set_active_room(next_room.item_id)
            break
    walk_step = 'rename'
    session['walk_step'] = walk_step
    return redirect(url_for('walkthrough.walk_steps'))
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

