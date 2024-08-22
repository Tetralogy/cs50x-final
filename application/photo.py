from flask import Blueprint, Flask, current_app, flash, render_template, request, jsonify, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from .database.models import User
from .extension import db
#FIXME: rename photo to upload and move annotate to annotate.py
photo = Blueprint('photo', __name__)

annotations = []

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@photo.route('/upload_form')
@login_required
def upload_form():
    print('upload_form called')
    return render_template('forms/upload_form.html.jinja')

@photo.route('/upload', methods=['POST'])
def upload():
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

@photo.route('/profile/upload', methods=['POST'])#FIXME
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
        return render_template('profile/uploaded.html.jinja', filename=filename)
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value

@photo.route('/media/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    print(f'files in {upload_folder}: {os.listdir(upload_folder)}')  # print the contents of the folder
    return send_from_directory(upload_folder, filename)

@photo.route('/view/<filename>')
@login_required
def view(filename):
    print(f'view called for filename: {filename}') 
    return render_template('media/view.html.jinja', image_url=f'/media/uploads/{filename}')

@photo.route('/annotate_form/<filename>')
@login_required
def annotate_form(filename):
    print('annotate_form called') 
    return render_template('forms/annotate.html.jinja', image_url=f'/media/uploads/{filename}')

@photo.route('/annotate', methods=['POST'])
def annotate():
    x = request.form.get('x')
    y = request.form.get('y')
    task = request.form.get('task')
    image = request.form.get('image')
    
    annotation = {'x': x, 'y': y, 'task': task, 'image': image}
    annotations.append(annotation)
    
    return render_template('tasklists/annotation_list.html.jinja', annotations=annotations)

@photo.route('/annotations')
def get_annotations():
    return render_template('tasklists/annotation_list.html.jinja', annotations=annotations)

#FIXME: make annotations link to tasks

@photo.route('/get_icons')
def get_icons():
    icons_folder = current_app.config['ICONS_FOLDER']
    icons = os.listdir(icons_folder)
    return render_template('/setup/icon_grid.html.jinja', icons=icons)

@photo.route('/media/icons/<filename>')
def get_icon_file(filename):
    icons_folder = current_app.config['ICONS_FOLDER']
    return send_from_directory(icons_folder, filename)

#FIXME: photo upload to profile

@photo.route('/set_profile_icon', methods=['PUT', 'POST'])#fixme
def set_profile_icon():
    if request.method == 'PUT':
        icon = request.form.get('icon')
        print(f'set_profile_icon called with icon: {icon}')
        current_user.profile_picture_url = icon
        db.session.commit()
        
        # Optionally, return some response or updated HTML
        return render_template('/profile/avatar.html.jinja') #jsonify(success=True)

@photo.route('/get_default_avatar')#doesn't work
def get_default_avatar():
    #TODO: make this a config option
    default_avatar_url = url_for('photo.get_icon_file', filename='person-circle.svg')
    print(f'default_avatar_url: {default_avatar_url}')
    return default_avatar_url
