from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required
from application.extension import db
from application.database.models import Room
from application.lists import get_userlist
from application.rooms import set_active_room

walkthrough = Blueprint('walkthrough', __name__)

@walkthrough.route('/walkthrough/setup', methods=['GET'])
@login_required
def walkthrough_setup():
    #2. #bug: user is prompted to select the floor and room they are currently in
    walk_setup = True
    session['walk_setup'] = walk_setup
    floor_list = get_userlist('Floor').entries
    return render_template('map/index.html.jinja', floor_list=floor_list, walk_setup=walk_setup)
    set_active_room(room_id)
    #3. #hack: user is given a choice to select in order which rooms to include in a full walkthrough
        #1. #hack: user taps each room to select the order
            #1. #fixme selected room gets block color change effect
                #2. #fixme number of the order selected is applied to the block as a badge
            #2. #fixme selected blocks can be unselected by clicking again
        #4. #todo: they can choose not to select the room order themselves
        
        #   1. order is then determined by the layout order of the blocks
        #5. #todo: once all rooms in the level are selected, the user is prompted to go to the next floor
        #   1. the user can choose to omit rooms if they navigate to another floor after making their selections for the current floor and confirming their selections when prompted
        #6. User confirms walkthrough order'''
    
    return render_template('')


@walkthrough.route('/walkthrough/start', methods=['POST'])
@login_required
def walk_start():
    if request.method == 'POST':
        active_room_id = request.form.get('active_room')
        if not active_room_id:
            first_room = current_user.active_home.active_floor.rooms.order_by(Room.id).first()
            print(f'first_room: {first_room.id}')
            active_room_id = first_room.id
        active_room = set_active_room(active_room_id)
        print(f'active_room: {active_room}')
        return render_template('walkthrough/index.html.jinja', active_room=active_room)

@walkthrough.route('/walkthrough/next', methods=['GET'])
@login_required
def walk_next():
    if not current_user.active_home.active_room:
        return 'No active room', 400
    
    next_room = current_user.active_home.active_floor.rooms.order_by(Room.order.asc()).filter(Room.order > current_user.active_home.active_room.order).first()
    if next_room:
        current_user.active_home.active_room = next_room
        db.session.commit()
    
    return render_template('onboarding/parts/home/walkthrough/parts/1confirm_room.html.jinja')

"""
Pseudo code for walkthrough
1. User starts walkthrough
2. User is asked to confirm the name and type of the room they are in
3. User is asked to upload a panorama picture of the room
4. User is asked to quickly add task drafts for the room
5. User is asked to add photos of areas in the room that contain tasks
6. User is asked to move to the next room
"""

