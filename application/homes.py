from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db
from application.database.models import Home, Floor


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
    if not floor_ids: #FIXME: if user has no floors
        print('home_levels is None')
    return render_template('onboarding/parts/home/attributes/floors/index.html.jinja')
    '''if not current_home.home_layout:
        print('home_layout is None')
        return render_template('onboarding/parts/home/attributes/layout_map.html.jinja')'''
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
            
            return render_template('onboarding/parts/home/attributes/name/home_name_text.html.jinja', home_name=active_home(new_active_home)) 
        else:
            home_query = select(Home).where(Home.home_id == current_user.active_home_id)
            home = db.session.execute(home_query).scalar_one_or_none()
            if home:
                home.home_name = new_home_name
                db.session.commit()
                return render_template('onboarding/parts/home/attributes/name/home_name_text.html.jinja', home_name=home.home_name)

@homes.route('/home/active', methods=['PUT'])
@login_required
def active_home(home_id):
    current_user.active_home_id = home_id
    home_query = select(Home).where(Home.home_id == home_id)
    home = db.session.execute(home_query).scalar_one_or_none()
    if home.user_id == current_user.id:
        current_user.active_home = home
        db.session.commit()
        return home.home_name #the name of the current active home
    

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
            raise NotImplementedError('floor_num not yet finished') #return render_template('onboarding/parts/home/attributes/floors/floor_form.html.jinja', new_floor_name = new_floor_name, new_floor_num = new_floor_num)
    if request.method == 'PUT':
        new_floor_name = request.form.get('new_floor_name')
        new_floor_number = request.form.get('new_floor_number')
        print(f'new_floor_name: {new_floor_name}, new_floor_num: {new_floor_number}')
                # Add validation to ensure values are not None
        if not new_floor_name or not new_floor_number:
            return "Error: 'new_floor_name' and 'new_floor_number' must be provided", 400
        
        floor = Floor(floor_name=new_floor_name, floor_number=new_floor_number)
        current_user.active_home.floors.append(floor)
        db.session.commit()
        return render_template('onboarding/parts/home/map/room_layout.html.jinja', floors=current_user.active_home.floors)
        
@homes.route('/home/floor/number', methods=['GET', 'PUT'])
@login_required
def floor_num():
    raise NotImplementedError('floor_num not yet finished')


@homes.route('/home/floor/rename/<int:floor_id>', methods=['PUT'])
@login_required
def edit_floor(floor_id):
    floor = db.get_or_404(Floor, floor_id)
    if not floor or floor.home.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    
    
    floor.floor_name = request.form.get('floor_name')
    db.session.commit()
    return render_template('onboarding/parts/home/map/room_layout.html.jinja', floors=current_user.active_home.floors)

@homes.route('/home/floors', methods=['GET'])
@login_required
def get_floors():
    floors = current_user.active_home.floors.all()
    return render_template('onboarding/parts/home/attributes/floors/floors_list.html.jinja', floors=floors)