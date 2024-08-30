from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import select
from application.extension import db
from application.database.models import Home


homes = Blueprint('homes', __name__)

@homes.route('/home/name', methods=['GET', 'POST', 'PUT'])
@login_required
def name_home():
    print(f'current_user.active_home_id: {current_user.active_home_id}')
    if request.method == 'GET':
        if not current_user.active_home:
            return render_template('profile/parts/new_home_button.html.jinja')
        new_home_name = current_user.active_home.home_name
        return render_template('profile/parts/home_rename_field.html.jinja', new_home_name = new_home_name)
    if request.method == 'POST':
        #request from the new home button
        return render_template('profile/parts/home_rename_field.html.jinja')
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
            
            return render_template('profile/parts/home_name_text.html.jinja', home_name=active_home(new_active_home)) 
        else:
            home_query = select(Home).where(Home.home_id == current_user.active_home_id)
            home = db.session.execute(home_query).scalar_one_or_none()
            if home:
                home.home_name = new_home_name
                db.session.commit()
                return render_template('profile/parts/home_name_text.html.jinja', home_name=home.home_name)

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
