from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required
from application.extension import db
from application.database.models import Room
from application.lists import get_list_entries_for_item, get_userlist
from application.rooms import set_active_room

walkthrough = Blueprint('walkthrough', __name__)

@walkthrough.route('/walkthrough/setup', methods=['GET'])
@login_required
def walkthrough_setup(): #BUG: NEED TO SANITIZE ROOM ORDER FOR EACH FLOOR BEFORE WALKTHROUGH
    walk_setup = True
    session['walk_setup'] = walk_setup
    floor_list = get_userlist('Floor').entries
    return render_template('map/index.html.jinja', floor_list=floor_list, walk_setup=walk_setup)


@walkthrough.route('/walkthrough/start', methods=['GET', 'POST'])
@login_required
def walk_start():
    active_room_id = request.form.get('active_room')
    active_room = set_active_room(active_room_id)
    print(f'active_room: {active_room}')
    walk_step = "rename"
    session['walk_step'] = walk_step
    return render_template('walkthrough/index.html.jinja', active_room=active_room)


@walkthrough.route('/walkthrough/steps', methods=['GET', 'PUT'])
@login_required
def walk_steps():
    if request.method == 'GET':
        walk_step = session.get('walk_step')
    if request.method == 'PUT':
        walk_step = request.form.get('walk_step')
        print(f'walk_step: {walk_step}')
        session['walk_step'] = walk_step
    return render_template(f'walkthrough/parts/{walk_step}.html.jinja', walk_step=walk_step)

@walkthrough.route('/walkthrough/next', methods=['GET'])
@login_required
def walk_next():
    if not current_user.active_home.active_room:
        return 'No active room', 400
    parent_entry_item_id = current_user.active_home.active_floor_id
    #current_user.active_home.active_room_id
    rooms_list = get_userlist('Room', parent_entry_item_id)
    print(f'rooms_list: {rooms_list}')
    rooms_list_ordered = sorted(rooms_list.entries, key=lambda x: x.order)
    print(f'rooms_list_ordered: {rooms_list_ordered}')
    current_active_room_list_entry = get_list_entries_for_item(current_user.active_home.active_room)[0]
    next_room_order = current_active_room_list_entry.order +1
    print(f'next_room_order: {next_room_order}')
    if next_room_order > len(rooms_list_ordered) - 1:
        next_room_order = 0
    next_room_list_entry = rooms_list_ordered[next_room_order]
    print(f'next_room_list_entry: {next_room_list_entry.item_id} {next_room_list_entry.get_item().name} {next_room_list_entry.order}')
    if not next_room_list_entry:
        raise Exception('No next room')
    next_room_id = next_room_list_entry.item_id
    active_room = set_active_room(next_room_id)
    
    return render_template('walkthrough/index.html.jinja', active_room=active_room)
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

