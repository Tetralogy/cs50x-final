from flask import Blueprint, render_template
from flask_login import current_user, login_required


onboard = Blueprint('onboard', __name__)

@onboard.route('/onboarding', methods=['GET'])
@login_required
def onboarding():
    print('onboarding called')
    if current_user.profile_picture_url is None:
        print('profile_picture_url is None')
        return render_template('onboarding/parts/upload_profile_photo.html.jinja')
    home_ids = [home.home_id for home in current_user.homes]
    print(f'homes: {home_ids}')
    if not home_ids:
        print('homes is empty')
        return render_template('onboarding/parts/home/index.html.jinja')
    return render_template('onboarding/parts/home/index.html.jinja') #temporary
    
    '''get the current home id when it is created
    room_ids = [room.room_id for room in current_user.room_ids]
    if not room_ids:
        print('rooms is empty')
        return render_template('onboarding/parts/room/index.html.jinja')'''
    

        
    '''home_query = select(Home).where(Home.user_id == current_user.id)
    home_id = db.session.execute(home_query).scalars().first()
    
    if currentuser has no home id
    if current_user has no room id
    if current_user has no tasks
    if current_user has no status'''
    """ raise NotImplementedError("onboarding not yet implemented") """
    #return '', 204
    
@onboard.route('/start', methods=['GET'])
@login_required
def start():
    return render_template('onboarding/index.html.jinja')