from datetime import datetime
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from application.database.models import Home, Room, Task, User, UserStatus
from application.utils import apology
from .extension import db


crud = Blueprint('crud', __name__)

@crud.route('/create_task', methods=['POST'])
@login_required
def create_task():   
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
            
            if room_id == None: #if no room is selected, place task in task orphanage to be adopted by a home+room later
                orphanage_query = select(Home).where(Home.home_name == "Orphanage")
                orphanage_home = db.session.execute(orphanage_query).scalars().first()
                if orphanage_home is None:
                    orphanage_home = Home(user_id=current_user.id, home_name="Orphanage")
                    db.session.add(orphanage_home)
                    db.session.commit()
                
                orphan_room_query = select(Room).where(Room.room_name == "Orphan")
                orphan_room = db.session.execute(orphan_room_query).scalars().first()
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

            if new_task.task_title == '' or new_task.task_title is None:
                last_task_query = select(Task).where(Task.user_id == current_user.id).order_by(Task.task_id.desc()).limit(1)
                last_task = db.session.execute(last_task_query).scalar_one_or_none()
                if last_task is not None:
                    new_task.task_title = f'Task #{int(last_task.task_id) + 1}'
                else:
                    new_task.task_title = 'Task #1'
                db.session.commit()
            
            db.session.add(new_task)
            db.session.commit()
            print(f"Task {new_task.task_id} created successfully")
            
            flash(f"task_title: {new_task.task_title} successfully created", category="success")
            return render_template('/tasklists/task_cells.html.jinja',task = new_task)

        except Exception as e:
            flash(str(e))
            return redirect(url_for('main.index'))

@crud.route('/create_task_form', methods=['GET'])
@login_required
def create_task_form():
    return render_template('forms/create_task_form.html.jinja')

@crud.route('/get_tasks/', methods=['GET'])
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
    tasks_query = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .limit(tasks_per_page)
        .offset(offset)
    )
    tasks = db.session.execute(tasks_query).scalars().all()

    print(f'Tasks retrieved: {len(tasks)}')
    for task in tasks:
        print(f'Task ID: {task.task_id}, Title: {task.task_title}')
    
    # Render the template with the retrieved tasks
    return render_template("tasklists/task_rows.html.jinja", tasks=tasks, page=page)

'''def fetch_task_by_id(task_id):
    task_query = select(Task).where(Task.task_id == task_id)
    task = db.session.execute(task_query).scalar_one_or_none()
    return task
'''
@crud.route('/get_task/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    task = db.get_or_404(Task, task_id)
    
    if not task or task.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    
    return render_template('tasklists/task_cells.html.jinja', task=task)

# Route to render the update task form
@crud.route('/edit_task/<int:task_id>', methods=['GET'])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    print(f'edit_task called for task_id: {task_id}')
    if not task or task.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    return render_template('forms/edit_task_form.html.jinja', task=task)

# Route to handle the update task form submission
@crud.route('/update_task/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    print(f'update_task called for task_id: {task_id}')
    task = db.get_or_404(Task, task_id)
    if not task or task.user_id != current_user.id:
        return jsonify({"success": False, "error": "Task not found or unauthorized"}), 404
    
    task_due_time_str = request.form.get('task_due_time', '')
    task_due_time = datetime.fromisoformat(task_due_time_str) if task_due_time_str else None
    
    task_scheduled_time_str = request.form.get('task_scheduled_time', '')
    task_scheduled_time = datetime.fromisoformat(task_scheduled_time_str) if task_scheduled_time_str else None
    
    #completed_at_str = request.form.get('completed_at')
    #completed_at = datetime.fromisoformat(completed_at_str) if completed_at_str else None

    task.task_title = request.form.get('task_title')
    task.task_description = request.form.get('task_description')
    task.task_due_time = task_due_time
    task.task_priority = request.form.get('task_priority')
    task.task_status = request.form.get('task_status')
    task.task_tags = request.form.get('task_tags')
    task.task_scheduled_time = task_scheduled_time
    #task.completed_at = completed_at

    db.session.commit()
    print('Task updated successfully?')
    return render_template('tasklists/task_cells.html.jinja', task=task), 200


@crud.route('/delete_task/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    if task is None:
        flash(f"task_id: {task_id} does not exist in the database", category="danger")
    if task.user_id != current_user.id:
        return apology("Unauthorized", 403)

    db.session.delete(task)
    db.session.commit()
    flash(f"task_id: {task_id} successfully deleted", category="success")
    print(f"Flash message created: Task {task_id} deleted successfully")

    return "", 200