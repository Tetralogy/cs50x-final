import os
from flask import Blueprint, flash, json, jsonify, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import case, select
from application.extension import db
from application.database.models import Custom, Home, Floor, Room


homes = Blueprint('homes', __name__)

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

@homes.route('/home/map', methods=['GET'])
@login_required
def get_map():
    floors_without_rooms = db.session.execute(select(Floor).where(Floor.home_id == current_user.active_home_id).where(~Floor.rooms.any())).scalars().all()
    if floors_without_rooms:
        edit_floor_layout(floors_without_rooms[0].floor_id)
    return render_template('map/index.html.jinja', floors=current_user.active_home.floors.all())


