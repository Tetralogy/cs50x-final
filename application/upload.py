import time
from flask import Blueprint, Flask, current_app, flash, render_template, request, jsonify, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

from application.list_utils import add_item_to_list, create_user_list, get_list_entries_for_item, get_userlist
from .database.models import Room, User
from .extension import db
from logs.logging_config import ApplicationLogger

upload = Blueprint('upload', __name__)
logger = ApplicationLogger.get_logger(__name__)

@upload.route('/upload/<string:item_model>', methods=['POST'])
@login_required
def upload_photo(item_model):
    photos = request.files.getlist('room_photos')
    if 'room_photos' not in request.files:
        logger.debug('No file part')
        return 'No file part'
    if not photos:
        logger.debug('No selected files')
        return 'No selected files'
    room_id = request.form.get('room_id')
    if not room_id:
        room_id = current_user.active_home.active_room_id
    logger.debug(f'room_id: {room_id}')
    room = db.get_or_404(Room, room_id)
    room_name = room.name
    list_name = f'{room_name} {item_model}s'
    parent_entry_id = get_list_entries_for_item(room, user_id=current_user.id)[0].id
    userlist = get_userlist(item_model, list_name, parent_entry_id) 
    if not userlist:
        userlist = create_user_list(item_model, list_name, parent_entry_id)
    new_items = []
    for photo in photos:
        if photo.filename == '':
            logger.debug('No selected file')
            
        if photo and not allowed_file(photo.filename):
            logger.debug(f'Unexpected file type: {photo.filename}')
            
        if photo and allowed_file(photo.filename):
            filename = f"{current_user.id}_{int(time.time())}_{secure_filename(photo.filename)}"
            logger.debug(f'Filename 1: {filename}')
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            # Check for duplicate filename and generate a unique one if needed
            base, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(file_path):
                new_filename = f"{base}_{counter}{extension}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
                counter += 1
            filename = os.path.basename(file_path)
            logger.debug(f'Filename 2: {filename}')
            logger.debug(f'File size before saving: {len(photo.read())} bytes')  # Check file size
            photo.seek(0)  # Reset file pointer to the beginning
            try:
                photo.save(file_path)
                file_size_after_upload = os.path.getsize(file_path)
                logger.debug(f'File size after saving: {file_size_after_upload} bytes') # double Check file size
            except Exception as e:
                logger.debug(f"Error saving file: {e}")
                
            logger.debug(f'File saved: {filename}')
            photo_url = url_for('upload.uploaded_file', filename=filename)
            logger.debug(f'Photo URL: {photo_url}')
            flash(f'{filename} uploaded', 'success')
            
            room_photo_count = int(len(userlist.entries))
            logger.debug(f'room_photo_count: {room_photo_count}')
            name = f"{filename} {current_user.active_home.active_room.name} {item_model} {room_photo_count + 1}"
            logger.debug(f'name (create_new_default): {name}')
            
            item_id = None
            order_index = None
            
            new_item = add_item_to_list(userlist.id, item_model, item_id, order_index, name, photo_url=photo_url)
            
            new_items.append(new_item)

    return render_template('lists/uploaded_list.html.jinja', entries=new_items, view='selectcoverphoto')
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
        
@upload.route('/media/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    logger.debug(f'files in {upload_folder}: {os.listdir(upload_folder)}')  # print the contents of the folder
    return send_from_directory(upload_folder, filename)



#old------------------------------------------------------------------------------------------#

@upload.route('/profile/upload', methods=['POST'])
def profile_upload():
    if 'file' not in request.files:
        logger.debug('No file part')
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        logger.debug('No selected file')
        return 'No selected file'
    if file and not allowed_file(file.filename):
        logger.debug(f'Unexpected file type: {file.filename}')
        return 'Unexpected file type', 415
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        logger.debug(f'File saved: {filename}')
        flash (f'{filename} uploaded', 'success')
        return render_template('profile/parts/uploaded.html.jinja', filename=filename)
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value


@upload.route('/view/<filename>')
@login_required
def view(filename):
    logger.debug(f'view called for filename: {filename}') 
    return render_template('media/view.html.jinja', image_url=f'/media/uploads/{filename}')



@upload.route('/get_icons')
def get_icons():
    icons_folder = current_app.config['ICONS_FOLDER']
    icons = os.listdir(icons_folder)
    return render_template('profile/parts/icon_grid.html.jinja', icons=icons)

@upload.route('/media/icons/<filename>')
def get_icon_file(filename):
    icons_folder = current_app.config['ICONS_FOLDER']
    return send_from_directory(icons_folder, filename)



@upload.route('/set_profile_icon', methods=['PUT', 'POST'])
def set_profile_icon():
    if request.method == 'PUT':
        icon = request.form.get('icon')
        logger.debug(f'set_profile_icon called with icon: {icon}')
        current_user.profile_picture_url = icon
        db.session.commit()
        return render_template('/profile/parts/avatar.html.jinja')

