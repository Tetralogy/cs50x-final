from flask import Blueprint, render_template, request
from flask_login import login_required


annotate = Blueprint('annotate', __name__)

@annotate.route('/annotate_form/<filename>')
@login_required
def annotate_form(filename):
    print('annotate_form called') 
    return render_template('forms/annotate.html.jinja', image_url=f'/media/uploads/{filename}')

@annotate.route('/annotate', methods=['POST'])
def annotate_image():
    x = request.form.get('x')
    y = request.form.get('y')
    task = request.form.get('task')
    image = request.form.get('image')
    
    annotations = []
    annotation = {'x': x, 'y': y, 'task': task, 'image': image}
    annotations.append(annotation)
    
    return render_template('tasklists/annotation_list.html.jinja', annotations=annotations)

@annotate.route('/annotations')
def get_annotations(annotations):
    return render_template('tasklists/annotation_list.html.jinja', annotations=annotations)

#FIXME: make annotations link to tasks