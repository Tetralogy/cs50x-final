from datetime import datetime
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, request, session, url_for, Blueprint, current_app
from functools import wraps
from flask_login import current_user, login_required
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from application.database.models import Home, Room, Task, User
from .utils import check_prerequisites, handle_error, apology, prerequisites_met
from .extension import db
from .database.schemas import task_schema, user_schema  # Import other schemas as needed
from logs.logging_config import ApplicationLogger

main = Blueprint('main', __name__)
logger = ApplicationLogger.get_logger(__name__)

# Register the error handler
main.errorhandler(Exception)(handle_error)


@main.route('/')
@login_required
@check_prerequisites
def index():
    return redirect(url_for('map.home_map'))

@main.route('/nav', methods=['GET']) # bottom nav buttons
def nav():
    return render_template('base/parts/nav/constructor.jinja')

@main.route('/debug', methods=['PUT'])
@login_required
def debug():
    current_user.debug = not current_user.debug
    db.session.commit()
    logger.debug(f'debug toggled: {current_user.debug}')
    return '', 204

@main.route('/tasks', methods=['GET'])
@login_required
def tasklist():
    #show all tasks
    #gather all tasks for the current user
    #organize them by room
    view = 'text-hierarchy'
    session['view'] = view
    return render_template('tasks/index.html.jinja')
    raise NotImplementedError("tasklist not yet implemented")
    
@main.route('/sitemap', methods=['GET']) # attempt to see all used routes
@login_required
def sitemap():
    links = []
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_for(rule.endpoint, _external=True)
            links.append(url)
    return render_template('base/parts/sitemap.html', links=links)