from flask import Flask, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required

from application.database.models import Home, Room, Task, User, UserSchedule, UserStatus
from .utils import handle_error, apology

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
    # Fetch user data
    user = User.query.get(current_user.id)
    
    # Fetch home data
    home = Home.query.filter_by(user_id=user.id).first()
    
    # Fetch rooms data
    rooms = Room.query.filter_by(home_id=home.home_id).all() if home else []
    
    # Fetch tasks data
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.task_due_time).limit(5).all()
    
    # Fetch user status
    user_status = UserStatus.query.filter_by(user_id=user.id).order_by(UserStatus.last_updated.desc()).first()
    
    # Fetch user schedule
    user_schedule = UserSchedule.query.filter_by(user_id=user.id).order_by(UserSchedule.start_time).limit(3).all()
    
    # todo add all data columns here
    
        
class User(db.Model, User
    id: Mapped[int] = map
    username: Mapped[str]
    email: Mapped[str] = 
    password_hash: Mapped
    profile_picture_url: 
    created_at: Mapped[da
    last_login: Mapped[da
                       
                       #todo joinedload FOR ALL TABLES IN 1 LINE
    users = User.query.options(joinedload(User.tasks)).all()
    
    return render_template('index.html', user=user)
                           user=user, 
                           home=home, 
                           rooms=rooms, 
                           tasks=tasks, 
                           user_status=user_status, 
                           user_schedule=user_schedule)


@main.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    pass
'''
    if request.method == 'POST':
        house_size = request.form.get('house_size')
        number_of_levels = request.form.get('number_of_levels')
        layout = request.form.get('layout')
        important_rooms = request.form.getlist('important_rooms')
        bedrooms = request.form.getlist('bedrooms')
        bathrooms = request.form.getlist('bathrooms')
        kitchen = request.form.getlist('kitchen')
        others = request.form.getlist('others')
        user_abilities = request.form.get('user_abilities')
# TODO: #18 edit the models to have rooms as an item and room-type as a value instead of "bathroom/bedroom/kitchen"etc.
        # Save the user's data to the database

        

        # Insert the important rooms into the database
        for room in important_rooms:
            db.session.add(UserImportantRoom(user_id=user.id, room=room))

        # Insert the bedrooms into the database
        for bedroom in bedrooms:
            db.session.add(UserBedroom(user_id=user.id, bedroom=bedroom))

        # Insert the bathrooms into the database
        for bathroom in bathrooms:
            db.session.add(UserBathroom(user_id=user.id, bathroom=bathroom))

        # Insert the kitchen into the database
        for kitchen_item in kitchen:
            db.session.add(UserKitchen(user_id=user.id, kitchen_item=kitchen_item))

        # Insert the others into the database
        for other in others:
            db.session.add(UserOther(user_id=user.id, other=other))

        # Commit the changes to the database
        db.session.commit()
        return render_template('onboarding_complete.html')

    return render_template('onboarding.html')
        
@main.route('/walkthrough', methods=['GET', 'POST'])
@login_required
def walkthrough():
    if request.method == 'POST':
        # Systematically go to every room in the house to note workload
        rooms = [
            'bedroom',
            'bathroom',
            'kitchen',
            'living_room',
            'dining_room',
            'home_office',
            'laundry_room',
            'garage',
            'other'
        ] # TODO: #19 edit this to match the models
        for room in rooms:
            workload = request.form.get(room)
            db.session.add(Walkthrough(
                user_id=current_user.id,
                room=room,
                workload=workload
            ))
        db.session.commit()

    # Retrieve the walkthrough data from the database
    walkthrough_data = Walkthrough.query.filter_by(user_id=current_user.id).all()

    return render_template('walkthrough.html', walkthrough_data=walkthrough_data)

        # TODO: #12 Annotation and organization of tasks
@main.route('/annotate', methods=['GET', 'POST'])
@login_required
def annotate():
    if request.method == 'POST':
        # Retrieve the form data
        room = request.form.get('room')
        x_coordinate = request.form.get('x_coordinate')
        y_coordinate = request.form.get('y_coordinate')
        annotation_text = request.form.get('annotation_text')

        # Create a new TaskAnnotation object and add it to the database
        task_annotation = TaskAnnotation(
            user_id=current_user.id,
            room=room,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            annotation_text=annotation_text
        )
        db.session.add(task_annotation)
        db.session.commit()

    # Retrieve the task annotations for the current user
    task_annotations = TaskAnnotation.query.filter_by(user_id=current_user.id).all()

    return render_template('annotate.html', task_annotations=task_annotations)

@main.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    # Get the walkthrough data for the current user
    walkthrough_data = Walkthrough.query.filter_by(user_id=current_user.id).all()

    # Calculate the total workload for each room
    room_workload = {}
    for walkthrough in walkthrough_data:
        room = walkthrough.room
        workload = walkthrough.workload
        if room in room_workload:
            room_workload[room] += workload
        else:
            room_workload[room] = workload

    # Calculate the relative workload for each room
    total_workload = sum(room_workload.values())
    room_relative_workload = {room: workload / total_workload for room, workload in room_workload.items()}

    # Get the task annotations for the current user
    task_annotations = TaskAnnotation.query.filter_by(user_id=current_user.id).all()

    # Group the task annotations by room
    room_task_annotations = {}
    for task_annotation in task_annotations:
        room = task_annotation.room
        if room in room_task_annotations:
            room_task_annotations[room].mainend(task_annotation)
        else:
            room_task_annotations[room] = [task_annotation]

    return render_template('map.html', room_workload=room_relative_workload, room_task_annotations=room_task_annotations)

#TODO: #15 A master task list is generated
@main.route('/tasklist', methods=['GET', 'POST'])
@login_required
def tasklist():
    # Get all tasks for the current user
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    # Generate a master task list
    master_task_list = []
    for task in tasks:
        task_annotation = TaskAnnotation.query.filter_by(task_id=task.id).first()
        if task_annotation:
            master_task_list.mainend({
                'task_id': task.id,
                'title': task.title,
                'description': task.description,
                'scheduled_time': task.scheduled_time,
                'priority': task.priority,
                'completed': task.completed,
                'product_recommendation_id': task.product_recommendation_id,
                'room': task_annotation.room,
                'workload': task_annotation.workload,
                'urgency_score': task_annotation.urgency_score,
                'task_tags': task_annotation.task_tags,
                'task_comments': task_annotation.task_comments,
                'task_attachments': task_annotation.task_attachments,
                'task_collaborators': task_annotation.task_collaborators,
                'task_recurring_pattern': task_annotation.task_recurring_pattern,
                'task_subtasks': task_annotation.task_subtasks,
                'task_notes': task_annotation.task_notes,
            })

    return render_template('tasklist.html', master_task_list=master_task_list)

#TODO: #16 create customtips and tricks and suggestions schema
'''