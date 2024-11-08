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
    #return redirect('/walkthrough/Dining Room 1/quicknote') #temporary for testing #xxx:remove when done
    #return redirect(url_for('homes.home_setup'))
    return redirect(url_for('rooms.map'))
    #return render_template('homes/create_home.html.jinja') #temporary
    #return render_template('dashboard/index.html.jinja', user=current_user, page=1)
    '''print('index called')
    home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    if home_id is not None:
        return render_template('dashboard/index.html.jinja', user=current_user, page=1) #[ ]: create user home page/dashboard
    
    return render_template('onboarding/index.html.jinja', user=current_user, onboarded=False)#[ ]: complete onboarding loop'''







@main.route('/tasks', methods=['GET'])
@login_required
def tasklist():
    #show all tasks
    #gather all tasks for the current user
    
    #organize them by room
    view = 'text-hierarchy'
    session['view'] = view
    return render_template('tasks/index.html.jinja')
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
    
@main.route('/sitemap', methods=['GET'])
@login_required
def sitemap():
    links = []
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_for(rule.endpoint, _external=True)
            links.append(url)
    return render_template('base/parts/sitemap.html', links=links)

# [ ] cleanup unused routes when done and tested