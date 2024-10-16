from flask import Blueprint, Flask, current_app, flash, render_template, request, jsonify, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from .database.models import User
from .extension import db

upload = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload.route('/upload_form')
@login_required
def upload_form():
    print('upload_form called')
    return render_template('forms/upload_form.html.jinja')

@upload.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('No file part')
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return 'No selected file'
    if file and not allowed_file(file.filename):
        print(f'Unexpected file type: {file.filename}')
        return 'Unexpected file type', 415
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(f'File saved: {filename}')
        flash (f'{filename} uploaded', 'success')
        return render_template('forms/uploaded.html.jinja', filename=filename)
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value

@upload.route('/profile/upload', methods=['POST'])
def profile_upload():
    if 'file' not in request.files:
        print('No file part')
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return 'No selected file'
    if file and not allowed_file(file.filename):
        print(f'Unexpected file type: {file.filename}')
        return 'Unexpected file type', 415
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(f'File saved: {filename}')
        flash (f'{filename} uploaded', 'success')
        return render_template('profile/parts/uploaded.html.jinja', filename=filename)
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value

@upload.route('/media/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    print(f'files in {upload_folder}: {os.listdir(upload_folder)}')  # print the contents of the folder
    return send_from_directory(upload_folder, filename)

@upload.route('/view/<filename>')
@login_required
def view(filename):
    print(f'view called for filename: {filename}') 
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
        print(f'set_profile_icon called with icon: {icon}')
        current_user.profile_picture_url = icon
        db.session.commit()
        
        # Optionally, return some response or updated HTML
        return render_template('/profile/parts/avatar.html.jinja') #jsonify(success=True)

'''@upload.route('/get_default_avatar')#doesn't work
def get_default_avatar():
    #[ ]: make this a config option
    default_avatar_url = url_for('upload.get_icon_file', filename='person-circle.svg')
    print(f'default_avatar_url: {default_avatar_url}')
    return default_avatar_url'''
