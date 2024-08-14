from flask import Blueprint, Flask, current_app, render_template, request, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

photo = Blueprint('photo', __name__)

annotations = []

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@photo.route('/upload-photo')
@login_required
def index():
    print('index called') 
    return render_template('forms/upload.html.jinja')

@photo.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        print('No file part')
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print(f'File saved: {filename}')
        return f'{filename} uploaded', 200
    return ("", 204)  # return empty response so htmx does not overwrite the progress bar value

'''@app.route('/annotate', methods=['POST'])
def annotate():
    x = request.form.get('x')
    y = request.form.get('y')
    task = request.form.get('task')
    image = request.form.get('image')
    
    annotation = {'x': x, 'y': y, 'task': task, 'image': image}
    annotations.append(annotation)
    
    return render_template('annotation_list.html', annotations=annotations)

@app.route('/annotations')
def get_annotations():
    return render_template('annotation_list.html', annotations=annotations)'''

#TODO: CLICK TO ANNOTATE
