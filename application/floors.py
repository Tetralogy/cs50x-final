from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import asc, func, select
from application.extension import db
from application.database.models import Floor, UserList
from application.list_utils import add_item_to_list, create_user_list, get_list_entries_for_item, get_userlist
from application.utils import check_prerequisites
from logs.logging_config import ApplicationLogger

floors = Blueprint('floors', __name__)
logger = ApplicationLogger.get_logger(__name__)

@floors.route('/home/floors/setup', methods=['GET', 'POST'])    # sends user to page to create a list of floors for the home
@login_required
#@check_prerequisites
def define_floors():
    if request.method == 'GET':
        multifloor = request.args.get('multifloor', '').lower() == 'true'
        if not current_user.active_home.floors.count(): # if home has no floors, 
            new_list = create_user_list('Floor', f'{current_user.active_home.name} Floors', get_list_entries_for_item(current_user.active_home)[0].id) # create floors list
            logger.debug(f'new_list: {new_list} (type: {type(new_list)})')
            new_floor = add_item_to_list(new_list.id, 'Floor') # create default floor and add to Floor userlist
            logger.debug(f'new_floor: {new_floor}')
            set_active_floor(new_floor.item_id) # set default floor as active
            set_ground_floor(new_floor.item_id)
            if not multifloor: # check if there should be multiple floors
                #set_ground_floor(new_floor.item_id)
                logger.debug(f'multifloor not: {multifloor}')
                return redirect(url_for('homes.home_setup'))
            return render_template('homes/create_floors.html.jinja', floor_list=new_list)
        floor_list = get_userlist('Floor') # if home_id has floors, get list of floors from userlists
        return render_template('homes/create_floors.html.jinja', floor_list=floor_list)
    if request.method == 'POST':
        ground_floor = request.form.get('ground_floor')
        set_ground_floor(ground_floor)
        set_active_floor(ground_floor)
        return redirect(url_for('homes.home_setup'))

@floors.route('/home/floor/<int:floor_id>/active', methods=['PUT', 'GET'])
@login_required
def set_active_floor(floor_id):
    logger.debug(f'set_active_floor called with floor_id: {floor_id}')
    #floor_query = select(Floor).where(Floor.id == floor_id)
    #floor = db.session.execute(floor_query).scalar_one_or_none()
    if not floor_id:
        floor_id = current_user.active_home.active_floor_id
        if not floor_id:
            floor_id = current_user.active_home.floors[0].id
    floor = db.get_or_404(Floor, floor_id)
    if floor.home_id == current_user.active_home_id:
        current_user.active_home.active_floor = floor
        db.session.commit()
        logger.debug(f'current_user.active_home.active_floor: {current_user.active_home.active_floor}')
        return floor #the object of the current active floor
    
#@floors.route('/set_ground_floor/<int:floor_id>', methods=['PUT'])
#@login_required
def set_ground_floor(floor_id):
    if not floor_id:
        floor_id = current_user.active_home.floors[0].id
    floor = db.get_or_404(Floor, floor_id)
    if floor.home_id == current_user.active_home_id:
        current_user.active_home.ground_floor = floor
        db.session.commit()
        logger.debug(f'current_user.active_home.ground_floor: {current_user.active_home.ground_floor}')
        return floor #the object of the current ground floor

@floors.route('/set_active_and_ground_floor/<int:floor_id>', methods=['PUT'])
@login_required
def set_active_and_ground_floor(floor_id):
    floor = set_active_floor(floor_id)
    floor = set_ground_floor(floor_id)
    return '', 200

@floors.route('/get_ground_floor_entry_id', methods=['GET'])
@login_required
def get_ground_floor_entry_id():
    if not current_user.active_home.ground_floor:
        #return '', 404
        set_ground_floor(current_user.active_home.floors[0].id)
    floor_entry_id = get_list_entries_for_item(current_user.active_home.ground_floor, 'Floor', current_user.id)[0].id
    logger.debug(f'get_ground_floor_entry_id called {floor_entry_id}')
    return str(floor_entry_id), 200
    
@floors.route('/floorplan/<int:floor_id>', methods=['GET'])
@login_required
def floorplan(floor_id):
    if not floor_id:
        floor_id = current_user.active_home.active_floor_id
    logger.debug(f'edit_floor_rooms called with floor_id: {floor_id}')
    floor = db.get_or_404(Floor, floor_id)
    set_active_floor(floor_id)
    if floor.home_id != current_user.active_home_id:
        raise Exception('Floor not associated with user home or unauthorized')
    #floor_list = get_userlist('Floor')
    return redirect(url_for('rooms.define_rooms', floor_id=floor_id))

@floors.route('/floorplan/<string:direction>', methods=['GET'])
@login_required
def get_next_floor(direction):
    if direction == 'next' or direction == 'up':
        direction = -1
    elif direction == 'prev' or direction == 'down':
        direction = +1
    floor_list = get_userlist('Floor')
    floor_list_ordered = sorted(floor_list.entries, key=lambda x: x.order)
    #users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    logger.debug(f'floor_list_ordered: {floor_list_ordered}')
    current_active_floor = db.get_or_404(Floor, current_user.active_home.active_floor_id) #current_user.active_home.active_floor
    current_active_floor_list_entry = get_list_entries_for_item(current_active_floor)[0]
    logger.debug(f'current_active_floor_list_entry: {current_active_floor_list_entry}')
    parent_entry_id = get_list_entries_for_item(current_user.active_home)[0].id
    floors_list = get_userlist('Floor', f'{current_user.active_home.name} Floors', parent_entry_id)
    logger.debug(f'floors_list: {floors_list}')
    floors_list_ordered = iter(sorted(floors_list.entries, key=lambda x: x.order))
    floors_list_ordered = sorted(floors_list.entries, key=lambda x: x.order)
    logger.debug(f'floors_list_ordered: {floors_list_ordered}')
    if not floors_list_ordered:
        # handle the case where the list is empty
        raise Exception('No rooms in the list')
    for i, floor in enumerate(floors_list_ordered):
        logger.debug(f'floor: {floor}')
        if floor == current_active_floor_list_entry:
            next_floor_index = (i + direction) % len(floors_list_ordered)
            next_floor = floors_list_ordered[next_floor_index]
            logger.debug(f'next_floor: {next_floor}')

            active_floor = set_active_floor(next_floor.item_id)
            logger.debug(f'active_floor 1: {active_floor}')
            break

    logger.debug(f'active_floor 2: {active_floor}')
    return redirect(url_for('floors.floorplan', floor_id=active_floor.id))