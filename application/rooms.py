import os
from flask import Blueprint, json, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db

from application.database.models import Custom, Floor, Room
from application.lists import create_user_list, get_userlist

rooms = Blueprint('rooms', __name__)

@rooms.route('/home/rooms/setup', methods=['GET', 'POST'])    # sends user to page to create a list of rooms for the home
@login_required
def define_rooms():
    if request.method == 'GET':
        if current_user.active_home.floors.count() == 1: # if home has one floor, 
            room_list = create_user_list('Room', f'{current_user.active_home.name} Rooms') # create rooms list
            print(f'room_list: {room_list} (type: {type(room_list)})')
            return render_template('homes/create_rooms.html.jinja', room_list=room_list)
        if current_user.active_home.floors.count() > 1:
            floor_list = get_userlist('Floor').entries # if home_id has floors, get list of floors from userlists
            for floor_entry in floor_list:
                print(f'floor list get floor_entry.id: {floor_entry.id}')
                print(f'floor list get floor_entry.get_item().name: {floor_entry.get_item().name}')
                room_list = create_user_list('Room', f'{current_user.active_home.name} {floor_entry.get_item().name} Rooms', floor_entry.id) # create rooms list
                print(f'room_list: {room_list} (type: {type(room_list)}) parent: {room_list.parent.get_item().name}')
            
            return render_template('homes/create_rooms.html.jinja', floor_list=floor_list)
    return 'define rooms', 200


    '''floor_list = get_userlist('Floor') # if home_id has floors, get list of floors from userlists
        return render_template('homes/create_floors.html.jinja', floor_list=floor_list)
    if request.method == 'POST':
        ground_floor = request.form.get('ground_floor')
        set_ground_floor(ground_floor)
        set_active_floor(ground_floor)
        return redirect(url_for('homes.home_setup'))'''

@rooms.route('/home/room/<int:room_id>/active', methods=['PUT'])
@login_required
def set_active_room(room_id):
    current_user.active_home.active_room_id = room_id
    room_query = select(Room).where(Room.room_id == room_id)
    room = db.session.execute(room_query).scalar_one_or_none()
    if room.home_id == current_user.active_home_id:
        current_user.active_home.active_room = room
        db.session.commit()
        print(f'current_user.active_home.active_room: {current_user.active_home.active_room}')
        return room #the object of the current active room
    
#____________________________________________________________________________________________________________________#




@rooms.route('/home/map/sort/<int:floor_id>', methods=['PUT'])
@login_required
def update_map_layout(floor_id): 
    list_order = request.form.getlist('list_order')
    print(f'list_order: {list_order}')
    for index, room_id in enumerate(list_order):
        print(f'index: {index}, room_id: {room_id}')
        room = db.get_or_404(Room, room_id)
        print(f'room: {room}')
        room.order = index
    db.session.commit()
    floor = db.get_or_404(Floor, floor_id)
    raise NotImplementedError("update_map_layout not yet implemented")
    return render_template('onboarding/parts/home/map/list.html.jinja', floor=floor)

@rooms.route('/home/map/room/add/<int:floor_id>', methods=['POST'])
@login_required
def add_room(floor_id):
    floor = db.get_or_404(Floor, floor_id)
    if not floor or floor.home_id != current_user.active_home_id:
        return jsonify({"error": "Floor not found or unauthorized"}), 404
    added_room_type = request.form.get('added_room_type')
    
    print(f'added_room_type: {added_room_type}')
    
    if not added_room_type:
        return jsonify({"error": "added_room_type is empty"}), 400
    new_order = request.form.get('order')
    print(f'new_order: {new_order}')
    if not new_order:
        return jsonify({"error": "new_order is empty"}), 400
    # Check if the type of room already exists and increment for the new default name
    rooms_matching_type = db.session.execute(select(Room).where(Room.home_id == current_user.active_home_id).where(Room.room_type == added_room_type)).scalars().all()
    print(f'rooms_matching_type: {rooms_matching_type}')
    new_room_name = f'{added_room_type} {len(rooms_matching_type) + 1}'
    # Add the new room to the database
    new_room = Room(room_name=new_room_name, room_type=added_room_type, order=new_order, floor_id=floor_id)
    print(f'new_room: {new_room}')
    
    current_user.active_home.rooms.append(new_room)
    db.session.commit()

    # Return the new item's data
    return render_template('onboarding/parts/home/map/room_icon.html.jinja', floor=floor, room=new_room)
    return new_room_name, 201 #[ ]: create appropriate icon and labels in html
    return jsonify(
        id= new_room.room_id,
        name= new_room.room_name,
        floor= floor_id,
        order = new_room.order
    )
    
@rooms.route('/home/room/rename/<int:room_id>', methods=['GET', 'PUT'])
@login_required
def rename_room(room_id):
    room = db.get_or_404(Room, room_id)
    if request.method == 'GET':
        if not room or room.home_id != current_user.active_home_id:
            return jsonify({"success": False, "error": "Room not found or unauthorized"}), 404
        return render_template('onboarding/parts/home/map/room_rename_field.html.jinja', room=room)
    if request.method == 'PUT':
        new_room_name = request.form.get(f'input_room_name-{room.room_id}')
        if not new_room_name:
            return "Error: 'new_room_name' must be provided", 400
        room.room_name = new_room_name
        return render_template('onboarding/parts/home/map/room_name_text.html.jinja', room=room)
    
@rooms.route('/home/map/room/add/type', methods=['POST'])
@login_required
def add_room_type():
    custom_type = request.form.get('custom_type')
    print(f'custom_type: {custom_type}')
    if not custom_type:
        return jsonify({'error': 'custom_type is empty'}), 400
    custom_type = custom_type.strip()
    if not custom_type:
        return jsonify({'error': 'custom_type is empty'}), 400
    data_type = 'room'
    default_room_types = load_default(data_type)
    if custom_type in default_room_types:
        return jsonify({'error': 'custom_type already exists'}), 400
    print(f'load_user_custom: {load_user_custom(data_type)}')
    if custom_type in load_user_custom(data_type):
        return jsonify({'error': 'custom_type already exists'}), 400
    new_custom_type = Custom(name=custom_type, type='room', user_id=current_user.id)
    db.session.add(new_custom_type)
    db.session.commit()
    return render_template('onboarding/parts/home/map/room_types_list.html.jinja', room_types=get_room_types())
    
def load_default(types):
    with open(os.path.join(os.path.dirname(__file__), 'static', 'default.json')) as f:
        default_data = json.load(f)
        
        return default_data[types]
    
def load_user_custom(data_type):
    return db.session.execute(select(Custom.name).where(Custom.user_id == current_user.id).where(Custom.type == data_type)).scalars().all()

def get_room_types():
        data_type = 'room'
        default_room_types = load_default(data_type)
        
        #print(f'default_room_types: {default_room_types}')
        
        user_custom_room_types = load_user_custom(data_type)
        #print(f'user_custom_room_types: {user_custom_room_types}')
        room_types = default_room_types + ([(custom) for custom in user_custom_room_types])
        return room_types