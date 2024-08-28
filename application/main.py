from datetime import datetime
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import time
from application.database.models import Home, Room, Task, User, UserStatus
from .utils import handle_error, apology
from .extension import db
from .database.schemas import task_schema, user_schema  # Import other schemas as needed

main = Blueprint('main', __name__)

# Register the error handler
main.errorhandler(Exception)(handle_error)

# Define a context processor to make current_user available in every template
'''@main.context_processor
@login_required
def inject_current_user():
    onboarded = Home.query.filter_by(user_id=current_user.id).first() is not None
    return dict(current_user=current_user, onboarded=onboarded)'''

@main.route('/')
@login_required
def index():
    print('index called')
    home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    if home_id is not None:
        return render_template('showtasks.html', user=current_user, page=1) #TODO: create user home page/dashboard
    
    return render_template('setup/onboarding.html', user=current_user, onboarded=False)#TODO: complete onboarding loop

@main.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    '''home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    
    if current_user.profile_picture_url is None:
    if currentuser has no home id
    if current_user has no room id
    if current_user has no tasks
    if current_user has no status'''
    """ raise NotImplementedError("onboarding not yet implemented") """
    return '', 204

@main.route('/walkthrough', methods=['GET', 'POST'])
@login_required
def walkthrough():
    raise NotImplementedError("walkthrough not yet implemented")



@main.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    raise NotImplementedError("map not yet implemented")

@main.route('/tasklist', methods=['GET', 'POST'])
@login_required
def tasklist():
    raise NotImplementedError("tasklist not yet implemented")

'''
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

@main.route('/save-order', methods=['POST'])
@login_required
def save_order():
    items = request.form.getlist('item')
    list_id = request.form.get('list_id')
    
    try:
        with db.session.begin():
            for position, item_id in enumerate(items):
                reorder_item(list_id, item_id, position)
        
        return jsonify({'status': 'success', 'message': 'Order updated successfully'})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    from sqlalchemy import update
    
def reorder_item(list_id, item_id, new_position):
    # Get the current positions of items in the list
    stmt = select(tools_supplies).where(tools_supplies.c.room_id == list_id).order_by(tools_supplies.c.item_id)
    items = db.session.scalars(stmt).all()
    
    # Find the nearest positions
    lower_position = 0
    upper_position = (len(items) + 1) * 1000
    for i, item in enumerate(items):
        if item.item_id == item_id:
            items.pop(i)
            break
        if i + 1 < len(items) and items[i+1].item_id > new_position:
            lower_position = item.item_id
            upper_position = items[i+1].item_id
            break
    
    # Calculate new position
    new_actual_position = (lower_position + upper_position) // 2
    
    # Update the position of the moved item
    stmt = update(tools_supplies).where(tools_supplies.c.room_id == list_id, tools_supplies.c.item_id == item_id).values(item_id=new_actual_position)
    db.session.execute(stmt)
    db.session.commit()
    
    

    
def create_new_list(list_name):
    new_list = tools_supplies(room_id=None, item_name=list_name, item_type='custom_list', is_on_hand=True)
    db.session.add(new_list)
    db.session.commit()
    return new_list

@main.route('/create-new-list', methods=['POST'])
@login_required
def create_new_list_view():
    list_name = request.form.get('list_name')
    new_list = create_new_list(list_name)
    return jsonify({'status': 'success', 'message': 'New list created successfully'})'''