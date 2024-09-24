from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db
from application.database.models import Floor
from application.lists import add_item_to_list, create_user_list, get_userlist
from application.rooms import get_room_types

floors = Blueprint('floors', __name__)

@floors.route('/home/floors/setup', methods=['GET', 'POST'])    # sends user to page to create a list of floors for the home
@login_required
def define_floors():
    if request.method == 'GET':
        multifloor = request.args.get('multifloor', '').lower() == 'true'
        if not current_user.active_home.floors.count(): # if home has no floors, 
            new_list = create_user_list('Floor', f'{current_user.active_home.home_name} Floors') # create floors list
            print(f'new_list: {new_list} (type: {type(new_list)})')
            new_floor = add_item_to_list(new_list.id, 'Floor') # create default floor and add to Floor userlist
            print(f'new_floor: {new_floor}')
            set_active_floor(new_floor.item_id) # set default floor as active
            if not multifloor: # check if there should be multiple floors
                set_ground_floor(new_floor.item_id)
                print(f'multifloor not: {multifloor}')
                return redirect(url_for('homes.home_setup'))
            return render_template('homes/create_floors.html.jinja', floor_list=new_list)

        floor_list = get_userlist('Floor') # if home_id has floors, get list of floors from userlists
        return render_template('homes/create_floors.html.jinja', floor_list=floor_list)
    if request.method == 'POST':
        ground_floor = request.form.get('ground_floor')
        set_ground_floor(ground_floor)
        set_active_floor(ground_floor)
        return redirect(url_for('homes.home_setup'))

@floors.route('/home/floor/<int:floor_id>/active', methods=['PUT'])
@login_required
def set_active_floor(floor_id):
    floor_query = select(Floor).where(Floor.id == floor_id)
    floor = db.session.execute(floor_query).scalar_one_or_none()
    if floor.home_id == current_user.active_home_id:
        current_user.active_home.active_floor = floor
        db.session.commit()
        print(f'current_user.active_home.active_floor: {current_user.active_home.active_floor}')
        return floor #the object of the current active floor
        #[ ] user adds floors to the home
            #[ ] user names each floor uniquely to better identify them
            #[ ] user corrects the order of the floors as they are in the house
    #[ ] main floor/ground floor is set as the active floor by default
        #[ ] user can change the active floor by clicking on it
    #[ ] user confirms the home's list of floors/ continue to next step button
    #[ ] user is taken to the home map of the active floor
    
#@floors.route('/home/floor/ground', methods=['PUT'])
#@login_required
def set_ground_floor(floor_id):
    floor_query = select(Floor).where(Floor.id == floor_id)
    floor = db.session.execute(floor_query).scalar_one_or_none()
    if floor.home_id == current_user.active_home_id:
        current_user.active_home.ground_floor = floor
        db.session.commit()
        print(f'current_user.active_home.ground_floor: {current_user.active_home.ground_floor}')
        return floor #the object of the current ground floor
    
    

@floors.route('/floor/create/upper', methods=['POST'])
@login_required
def new_floor_upper():
    list_id = get_userlist('Floor')
    return add_item_to_list(list_id, 'Floor')    #create floor + add floor to floor list
    
    
    
#____________________________________________________________________________________________________________________#
    if request.method == 'GET':
        if db.session.execute(select(Floor).filter(Floor.home_id == current_user.active_home_id)).first(): #check if there is already a floor
            return 'Floor already exists', 204
        return create_floor() # create default ground floor
    if request.method == 'POST':
        return create_floor()
    
@floors.route('/home/floor/name', methods=['GET', 'PUT'])
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
        
@floors.route('/home/floor/number', methods=['GET', 'PUT'])
@login_required
def floor_num():
    raise NotImplementedError('floor_num not yet finished')


@floors.route('/home/floor/rename/<int:floor_id>', methods=['GET', 'PUT'])
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
    

@floors.route('/home/floors', methods=['GET'])
@login_required
def edit_floors_order():
    floors = current_user.active_home.floors.all()
    return render_template('onboarding/parts/home/attributes/floors/edit.html.jinja', floors=floors)


        
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


@floors.route('/home/floor/sort', methods=['PUT']) 
@login_required
def update_floor_order():
    new_order = request.form.getlist('order')
    print(f'new_order: {new_order}')
    if not new_order or not all(new_order):
        print("Invalid new order data")
        return jsonify({"error": "Invalid new order data"}), 400
    
    for index, floor_id in enumerate(new_order):
        if floor_id:  # Check if floor_id is not empty
            print(f'index: {index}, floor_id: {floor_id}')
            floor = Floor.query.get(int(floor_id)) 
            print(f'floor: {floor}')
            if floor:
                floor.order = index
            else:
                print(f"Floor not found for id {floor_id}")
    db.session.commit()

    print(f'floors returned: {floors}')
    return render_template('homes/list_floors.html.jinja')

@floors.route('/home/floor/delete/<int:floor_id>', methods=['DELETE'])
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
    
@floors.route('/home/floor/edit/<int:floor_id>', methods=['GET'])
@login_required
def edit_floor_layout(floor_id):
    print(f'edit_floor_rooms called with floor_id: {floor_id}')
    floor = db.get_or_404(Floor, floor_id)
    if not floor or floor.home_id != current_user.active_home_id:
        return jsonify({"error": "Floor not found or unauthorized"}), 404

    room_types = get_room_types()
    #print(f'default_data[types]: {type(room_types)}')
    #print(f'room_types after extension: {room_types}')
    set_active_floor(floor_id)
    return render_template('onboarding/parts/home/map/add_rooms.html.jinja', room_types=room_types, floor=floor) #: hx-push-url breaks the page

@floors.route('/home/floor/edit/next', methods=['GET'])
@login_required
def edit_floor_layout_next():
    current_floor = current_user.active_home.active_floor
    if not current_floor:
        print('No floor selected')
        return jsonify({"error": "No floor selected"}), 404
    next_floor_order = current_floor.order -1
    next_floor = db.session.execute(select(Floor).where(Floor.home_id == current_user.active_home_id).where(Floor.order == next_floor_order)).first()
    print(f'next_floor: {next_floor}')
    if not next_floor:
        print('No next floor')
        return jsonify({"error": "No next floor"}), 404
    floor_id = next_floor[0].floor_id
    
    return edit_floor_layout(floor_id)
#[ ]: cleanup unused code after floor and room setup is complete