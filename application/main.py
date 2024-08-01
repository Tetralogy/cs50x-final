from datetime import datetime
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
import time
from application.database.models import Home, Room, Task, User, UserStatus
from .utils import handle_error, apology
from .extension import db
from .database.schemas import task_schema, user_schema  # Import other schemas as needed

main = Blueprint('main', __name__)

# Register the error handler
main.errorhandler(Exception)(handle_error)

# Define a context processor to make current_user available in every template
@main.context_processor
def inject_current_user():
    onboarded = Home.query.filter_by(user_id=current_user.id).first() is not None
    return dict(current_user=current_user, onboarded=onboarded)

@main.route('/get-flash-messages')
def get_flash_messages():
    messages = get_flashed_messages(with_categories=True)
    print(f"Retrieved flash messages: {messages}")
    return render_template('flash_messages.html' , messages=messages)

@main.route('/remove-flash')
def remove_flash():
    return '', 200  # Return empty response

@main.route('/')
@login_required
def index():
    print('hello world testing!!!') 
    return render_template('showtasks.html', user=current_user, page=1)

@main.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    raise NotImplementedError("onboarding not yet implemented")


@main.route('/new_task', methods=['POST'])
@login_required
def new_task():   
    if request.method == "POST":
        try:
            task_due_time_str = request.form.get('task_due_time', '')
            task_due_time = datetime.fromisoformat(task_due_time_str) if task_due_time_str else None
            
            task_scheduled_time_str = request.form.get('task_scheduled_time', '')
            task_scheduled_time = datetime.fromisoformat(task_scheduled_time_str) if task_scheduled_time_str else None
            
            completed_at_str = request.form.get('completed_at')
            completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

            if completed_at:
                completed_at = datetime.fromisoformat(completed_at)
            else:
                completed_at = None
                
            room_id = request.form.get('room_id')
            if room_id == None:
                orphanage_home = Home.query.filter_by(home_name="Orphanage").first()
                if orphanage_home is None:
                    orphanage_home = Home(user_id=current_user.id, home_name="Orphanage")
                    db.session.add(orphanage_home)
                    db.session.commit()
                    
                orphan_room = Room.query.filter_by(room_name="Orphan", home_id=orphanage_home.home_id).first()
                if orphan_room is None:
                    orphan_room = Room(room_name="Orphan", home_id=orphanage_home.home_id)
                    db.session.add(orphan_room)
                    db.session.commit()

                orphanage_home.rooms.append(orphan_room)
                db.session.commit()

                room_id = orphan_room.room_id
            
            new_task = Task(
                room_id = room_id,
                task_title = request.form.get('task_title'),
                task_description = request.form.get('task_description'),
                task_created_at = request.form.get('task_created_at'),
                task_due_time = task_due_time,
                task_priority = request.form.get('task_priority'),
                task_status = request.form.get('task_status'),
                task_tags = request.form.get('task_tags'),
                task_scheduled_time = task_scheduled_time,
                completed_at = completed_at,
                user_id = current_user.id)
            
            db.session.add(new_task)
            db.session.commit()

            return jsonify(task_schema.dump(new_task))

        except Exception as e:
            flash(str(e))
            return redirect(url_for('main.index'))

@main.route('/get_tasks/', methods=['GET'])
@login_required
def get_tasks():
    print('get_tasks called')
    page = int(request.args.get("page", 1))
    print(f'page: {page}')
    
    # Define the number of tasks per page
    tasks_per_page = 10

    # Calculate the offset
    offset = (page - 1) * tasks_per_page

    # Retrieve tasks with limit and offset
    tasks = Task.query.filter_by(user_id=current_user.id).limit(tasks_per_page).offset(offset).all()
    
    print(f'Tasks retrieved: {len(tasks)}')
    for task in tasks:
        print(f'Task ID: {task.task_id}, Title: {task.task_title}')
    
    # Render the template with the retrieved tasks
    return render_template("task_rows.html", tasks=tasks, page=page)

@main.route('/get_task/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    
    if not task or task.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    
    return jsonify({
        "success": True,
        "task": task_schema.dump(task)
    }), 200
    
@main.route('/edit_task/<int:task_id>', methods=['PUT'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    
    if not task or task.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    
    data = request.get_json()
    
    try:
        # Validate the input data
        task_data = task_schema.load(data, partial=True, session=db.session)
    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400
    
    # Update the task with validated data
    for key, value in task_data.items():
        setattr(task, key, value)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    
    return jsonify({
        "success": True,
        "message": "Task updated successfully",
        "task": task_schema.dump(task)
    }), 200

@main.route('/delete_task/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task is None:
        flash(f"task_id: {task_id} does not exist in the database", category="danger")
    if task.user_id != current_user.id:
        return apology("Unauthorized", 403)

    db.session.delete(task)
    db.session.commit()
    flash(f"task_id: {task_id} successfully deleted", category="success")
    print(f"Flash message created: Task {task_id} deleted successfully")

    return "", 200

@main.route('/walkthrough', methods=['GET', 'POST'])
@login_required
def walkthrough():
    raise NotImplementedError("walkthrough not yet implemented")

@main.route('/annotate', methods=['GET', 'POST'])
@login_required
def annotate():
    raise NotImplementedError("annotate not yet implemented")

@main.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    raise NotImplementedError("map not yet implemented")

@main.route('/tasklist', methods=['GET', 'POST'])
@login_required
def tasklist():
    raise NotImplementedError("tasklist not yet implemented")