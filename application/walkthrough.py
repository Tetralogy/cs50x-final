from flask import Blueprint, render_template
from flask_login import current_user, login_required
from application.extension import db
from application.database.models import Room

walkthrough = Blueprint('walkthrough', __name__)

@walkthrough.route('/walkthrough/start', methods=['GET'])
@login_required
def walk_start():
    if not current_user.active_home.active_room:
        first_room = current_user.active_home.active_floor.rooms
        print(f'first_room: {first_room}')
        '''current_user.active_home.active_room = first_room
        db.session.commit()'''
    
    return render_template('walkthrough/parts/1confirm_room.html.jinja')

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

