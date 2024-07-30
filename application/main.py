from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload
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

@main.route('/')
@login_required
def index():
    return render_template('taskform.html', user=current_user)

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


@main.route('/edit_task/<int:task_id>', methods=['PUT']) #TODO: complete this route
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return apology("Unauthorized", 403)

    if request.method == 'GET':
        return jsonify(task_schema.dump(task))

    if request.method == 'PUT':
        try:
            data = request.json #fixme

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
            
            db.session.commit()
            return jsonify(task_schema.dump(task)), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


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

    return '', 200

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