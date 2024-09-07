from flask import Blueprint, render_template
from flask_login import current_user, login_required
from application.extension import db
from application.database.models import Room
from application.utils import detect_recursive_route
walkthrough = Blueprint('walkthrough', __name__)

@walkthrough.route('/walkthrough', methods=['GET'])
@login_required
@detect_recursive_route
def walk_start():
    if not current_user.active_home.active_room:
        first_room = current_user.active_home.active_floor.rooms
        print(f'first_room: {first_room}')
        '''current_user.active_home.active_room = first_room
        db.session.commit()'''
    
    return render_template('onboarding/parts/home/walkthrough/index.html.jinja')

