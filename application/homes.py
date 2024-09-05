import os
from flask import Blueprint, flash, json, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import case, select
from application.extension import db
from application.database.models import Custom, Home, Floor, Room


homes = Blueprint('homes', __name__)

@homes.route('/home/setup', methods=['GET'])
@login_required
def home_setup():
    if not current_user.active_home:
        return render_template('onboarding/parts/home/attributes/name/index.html.jinja')
    current_home = current_user.active_home
    print(f'current_home: {current_home} name: {current_home.home_name}')
    if not current_home.home_size_sqm:
        print('home_size_sqm is None')
        return render_template('onboarding/parts/home/attributes/size/index.html.jinja')
    
    floor_ids_query = select(Floor.floor_id).where(Floor.home_id == current_home.home_id)
    floor_ids = db.session.execute(floor_ids_query).scalars().all()
    print(f'floor_ids: {floor_ids}')
    if not floor_ids:
        print('home_levels is None')
        return render_template('onboarding/parts/home/attributes/floors/index.html.jinja')
    room_ids_query = select(Room.room_id).where(Room.home_id == current_home.home_id)
    room_ids = db.session.execute(room_ids_query).scalars().all()
    if not room_ids:
        print('home_layout is None')
        first_floor_id = db.session.execute(
            select(Floor.floor_id).where(Floor.home_id == current_home.home_id).order_by(Floor.order)
        ).scalar()
        if first_floor_id is None:
            raise ValueError('No floors in home')
        set_active_floor(first_floor_id)
        return render_template('onboarding/parts/home/map/index.html.jinja', floor=current_home.active_floor)#FIXME: ADD CONDITIONS FOR WHEN HOME HAS FLOORS AND WHEN HOME HAS ROOMS
    floors_without_rooms = db.session.execute(
        select(Floor.floor_id).where(Floor.home_id == current_home.home_id)
            .where(Floor.floor_id.not_in(select(Room.floor_id).where(Room.home_id == current_home.home_id)))
    ).scalars().all()
    print(f'floors_without_rooms: {floors_without_rooms}')
    if floors_without_rooms:
        first_floor_without_rooms = db.session.execute(
            select(Floor.floor_id).where(Floor.home_id == current_home.home_id)
                .where(Floor.floor_id.notin_(select(Room.floor_id).where(Room.home_id == current_home.home_id)))
                .order_by(Floor.order)
        ).scalar()
        if first_floor_without_rooms is None:
            raise ValueError('No floors without rooms')
        set_active_floor(first_floor_without_rooms)
        return render_template('onboarding/parts/home/map/index.html.jinja', floor=current_home.active_floor)
    return render_template('onboarding/parts/home/map/index.html.jinja', floor=current_home.active_floor)#temporary, 
    raise NotImplementedError('home_setup not yet finished')

@homes.route('/home/name', methods=['GET', 'POST', 'PUT'])
@login_required
def name_home():
    print(f'current_user.active_home_id: {current_user.active_home_id}')
    if request.method == 'GET':
        if not current_user.active_home:
            return render_template('onboarding/parts/home/attributes/name/new_home_button.html.jinja')
        new_home_name = current_user.active_home.home_name
        return render_template('onboarding/parts/home/attributes/name/home_rename_field.html.jinja', new_home_name = new_home_name)
    if request.method == 'POST':
        #request from the new home button
        return render_template('onboarding/parts/home/attributes/name/home_rename_field.html.jinja')
    if request.method == 'PUT':
        new_home_name = request.form.get('input_home_name')
        if not new_home_name:
            # Handle the case where home_name is None
            return "Home name is required", 400
        if not current_user.active_home_id:
            new_home = Home(user_id = current_user.id,
                            home_name = new_home_name)
            db.session.add(new_home)
            db.session.commit()
            
            new_active_home = new_home.home_id
            
            return render_template('onboarding/parts/home/attributes/name/home_name_text.html.jinja', home_name=set_active_home(new_active_home)) 
        else:
            home_query = select(Home).where(Home.home_id == current_user.active_home_id)
            home = db.session.execute(home_query).scalar_one_or_none()
            if home:
                home.home_name = new_home_name
                db.session.commit()
                return render_template('onboarding/parts/home/attributes/name/home_name_text.html.jinja', home_name=home.home_name)

@homes.route('/home/active', methods=['PUT'])
@login_required
def set_active_home(home_id):
    current_user.active_home_id = home_id
    home_query = select(Home).where(Home.home_id == home_id)
    home = db.session.execute(home_query).scalar_one_or_none()
    if home.user_id == current_user.id:
        current_user.active_home = home
        db.session.commit()
        print(f'current_user.active_home: {current_user.active_home}')
        return home.home_name #the name of the current active home
    
@homes.route('/home/floor/active', methods=['PUT'])
@login_required
def set_active_floor(floor_id):
    current_user.active_home.active_floor_id = floor_id
    floor_query = select(Floor).where(Floor.floor_id == floor_id)
    floor = db.session.execute(floor_query).scalar_one_or_none()
    if floor.home_id == current_user.active_home_id:
        current_user.active_home.active_floor = floor
        db.session.commit()
        print(f'current_user.active_home.active_floor: {current_user.active_home.active_floor}')
        return floor.floor_name #the name of the current active floor
    
@homes.route('/home/room/active', methods=['PUT'])
@login_required
def set_active_room(room_id):
    current_user.active_home.active_room_id = room_id
    room_query = select(Room).where(Room.room_id == room_id)
    room = db.session.execute(room_query).scalar_one_or_none()
    if room.home_id == current_user.active_home_id:
        current_user.active_home.active_room = room
        db.session.commit()
        print(f'current_user.active_home.active_room: {current_user.active_home.active_room}')
        return room.room_name #the name of the current active room

@homes.route('/home/size', methods=['GET', 'PUT'])
@login_required
def home_size():
    if request.method == 'GET':
        if not current_user.active_home:
            return render_template('onboarding/parts/home/attributes/size/new_home_button.html.jinja')
        print('clicked')
        return render_template('onboarding/parts/home/attributes/size/home_size_field.html.jinja')
    home_query = select(Home).where(Home.home_id == current_user.active_home_id)
    home = db.session.execute(home_query).scalar_one_or_none()
    if home:
        home.home_size_sqm = request.form.get('home_size_sqm')
        print(f'home_size_sqm: {home.home_size_sqm}')
        db.session.commit()
        return render_template('onboarding/parts/home/attributes/size/home_size_text.html.jinja', home_size_sqm=home.home_size_sqm)
    
    
@homes.route('/home/floor/name', methods=['GET', 'PUT'])
@login_required
def name_floor():
    current_home = current_user.active_home
    if request.method == 'GET':
        floor_ids_query = select(Floor.floor_id).where(Floor.home_id == current_home.home_id)
        floor_ids = db.session.execute(floor_ids_query).scalars().all()
        print(f'floor_ids: {floor_ids}')
        if not floor_ids:
            new_floor_name = 'default Floor'
            new_floor_num = 1
            floor = Floor(floor_name=new_floor_name, floor_number=new_floor_num)
            current_user.active_home.floors.append(floor)
            db.session.commit()
            return render_template('onboarding/parts/home/attributes/floors/floor_form.html.jinja', new_floor_name = new_floor_name, new_floor_num = new_floor_num)
    if request.method == 'PUT':
        new_floor_name = request.form.get('new_floor_name')
        new_floor_number = request.form.get('new_floor_number')
        print(f'new_floor_name: {new_floor_name}, new_floor_num: {new_floor_number}')
                # Add validation to ensure values are not None
        if not new_floor_name or not new_floor_number:
            return "Error: 'new_floor_name' and 'new_floor_number' must be provided", 400
        
@homes.route('/home/floor/number', methods=['GET', 'PUT'])
@login_required
def floor_num():
    raise NotImplementedError('floor_num not yet finished')


@homes.route('/home/floor/rename/<int:floor_id>', methods=['GET', 'PUT'])
@login_required
def rename_floor(floor_id):
    floor = db.get_or_404(Floor, floor_id)
    if request.method == 'GET':
        if not floor or floor.home_id != current_user.active_home_id:
            return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
        return render_template('onboarding/parts/home/attributes/floors/rename_field.html.jinja', floor=floor)
    if request.method == 'PUT':
        new_floor_name = request.form.get(f'input_floor_name-{floor.floor_id}')
        if not new_floor_name:
            return "Error: 'new_floor_name' must be provided", 400
        floor.floor_name = new_floor_name
        return render_template('onboarding/parts/home/attributes/floors/name_text.html.jinja', floor=floor)
    

@homes.route('/home/floors', methods=['GET'])
@login_required
def get_floors():
    floors = current_user.active_home.floors.all()
    return render_template('onboarding/parts/home/attributes/floors/edit.html.jinja', floors=floors)

@homes.route('/home/floor/new', methods=['GET', 'POST'])
@login_required
def new_floor():
    if request.method == 'GET':
        if db.session.execute(select(Floor).filter(Floor.home_id == current_user.active_home_id)).first():
            return 'Floor already exists', 204
        return create_floor()
    if request.method == 'POST':
        return create_floor()
        
def create_floor():
    highest_order_number = db.session.execute(select(db.func.max(Floor.order)).filter(Floor.home_id == current_user.active_home_id)).scalar()
    lowest_order_number = db.session.execute(select(db.func.min(Floor.order)).filter(Floor.home_id == current_user.active_home_id)).scalar()
    print(f'lowest_order_number: {lowest_order_number}')
    if lowest_order_number is not None or lowest_order_number == 0:
        new_order_number = lowest_order_number - 1
    else:
        new_order_number = 0
        
    new_floor_name = f'Floor {abs(highest_order_number + abs(lowest_order_number))+2}' if new_order_number != 0 else 'Ground Floor'
    print(f'new_floor_name: {new_floor_name}, new_order_num: {new_order_number}')
    # Add validation to ensure values are not None
    if not new_floor_name or new_order_number is None:
        return "Error: 'new_floor_name' and 'new_floor_number' must be provided", 400
    try:
        floor = Floor(floor_name=new_floor_name, order=new_order_number)
        current_user.active_home.floors.append(floor)
        db.session.commit()
    except Exception as e:
        print(f"Error creating floor: {e}")
        return "Error creating floor", 400
    return render_template('onboarding/parts/home/attributes/floors/row.html.jinja', floor=floor), 201


@homes.route('/home/floor/sort', methods=['POST'])
def update_order():
    new_order = request.form.getlist('order')
    print(f'new_order: {new_order}')
    for index, floor_id in enumerate(new_order):
        print(f'index: {index}, floor_id: {floor_id}')
        floor = Floor.query.get(int(floor_id))
        print(f'floor: {floor}')
        floor.order = index
    db.session.commit()
    floors = current_user.active_home.floors.all()
    print(f'floors returned: {floors}')
    return render_template('onboarding/parts/home/attributes/floors/list.html.jinja', floors=floors)

@homes.route('/home/floor/delete/<int:floor_id>', methods=['DELETE'])
@login_required
def delete_floor(floor_id):
    floor = db.get_or_404(Floor, floor_id)
    if not floor or floor.home_id != current_user.active_home_id:
        return jsonify({"error": "Floor not found or unauthorized"}), 404
    db.session.delete(floor)
    try:
        db.session.commit()
        flash(f"floor_id: {floor_id} successfully deleted", category="success")
        return jsonify({"message": "Floor deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@homes.route('/home/floor/edit/<int:floor_id>', methods=['GET'])
@login_required
def edit_floor_rooms(floor_id):
    print(f'edit_floor_rooms called with floor_id: {floor_id}')
    floor = db.get_or_404(Floor, floor_id)
    if not floor or floor.home_id != current_user.active_home_id:
        return jsonify({"error": "Floor not found or unauthorized"}), 404

    room_types = get_room_types()
    #print(f'default_data[types]: {type(room_types)}')
    #print(f'room_types after extension: {room_types}')
    set_active_floor(floor_id)
    return render_template('onboarding/parts/home/map/add_rooms.html.jinja', room_types=room_types, floor=floor) #FIXME: hx-push-url breaks the page

#FIXME: map layout of floors with rooms

@homes.route('/home/map', methods=['GET'])
@login_required
def get_map():
    floors_without_rooms = db.session.execute(select(Floor).where(Floor.home_id == current_user.active_home_id).where(~Floor.rooms.any())).scalars().all()
    if floors_without_rooms:
        edit_floor_rooms(floors_without_rooms[0].floor_id)
    return render_template('map/index.html.jinja', floors=current_user.active_home.floors.all())


@homes.route('/home/map/sort/<int:floor_id>', methods=['PUT'])
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
    return render_template('onboarding/parts/home/map/list.html.jinja', floor=floor)

@homes.route('/home/map/room/add/<int:floor_id>', methods=['POST'])
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
    # Check if the item already exists
    rooms_matching_type = db.session.execute(select(Room).where(Room.home_id == current_user.active_home_id).where(Room.room_type == added_room_type)).scalars().all()
    print(f'rooms_matching_type: {rooms_matching_type}')
    new_room_name = f'{added_room_type} {len(rooms_matching_type) + 1}'
    # Add the new item to the database
    new_room = Room(room_name=new_room_name, room_type=added_room_type, order=new_order, floor_id=floor_id)
    print(f'new_room: {new_room}')
    
    current_user.active_home.rooms.append(new_room)
    db.session.commit()

    # Return the new item's data
    return render_template('onboarding/parts/home/map/room_icon.html.jinja', floor=floor, room=new_room)
    return new_room_name, 201 #FIXME: create appropriate icon and labels in html
    return jsonify(
        id= new_room.room_id,
        name= new_room.room_name,
        floor= floor_id,
        order = new_room.order
    )
    
@homes.route('/home/room/rename/<int:room_id>', methods=['GET', 'PUT'])
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
    
@homes.route('/home/map/room/add/type', methods=['POST'])
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