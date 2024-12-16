import logging
from flask import Blueprint, flash, jsonify, render_template
from flask_login import current_user, login_required
from sqlalchemy import delete
from application.extension import db
from application.database.models import RoomDefault, Floor, UserList, UserListEntry, Home, Room, Photo, Task, Pin
from logs.logging_config import ApplicationLogger

account = Blueprint('account', __name__)

logger = ApplicationLogger.get_logger(__name__)

@account.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile/index.html.jinja')

@account.route('/account/reset', methods=['POST'])
@login_required
def reset_user_data():
    try:
        # Store the username and password_hash
        username, password_hash = current_user.username, current_user.password_hash
        # Delete all related data
        models_to_delete = [Pin, Task, Photo, Room, Home, Floor, RoomDefault, UserList, UserListEntry]
        
        for model in models_to_delete:
            if hasattr(model, 'user_id'):
                db.session.execute(delete(model).where(model.user_id == current_user.id))
            if hasattr(model, 'home_id'):
                db.session.execute(delete(model).where(model.home_id == current_user.active_home_id))
        # Reset the user's data
        current_user.profile_picture_url = None
        current_user.created_at = db.func.now()
        current_user.last_login = None
        current_user.username = username
        current_user.password_hash = password_hash
        current_user.active_home_id = None
        db.session.commit()
        flash("User data has been reset successfully", category="success")
        return render_template('profile/index.html.jinja')
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@account.route('/account/delete', methods=['DELETE'])
@login_required
def delete_user_account():
    try:
        # Delete all related data
        models_to_delete = [Pin, Task, Photo, Room, Home, Floor]
        for model in models_to_delete:
            if hasattr(model, 'user_id'):
                db.session.execute(delete(model).where(model.user_id == current_user.id))
            if hasattr(model, 'home_id'):
                db.session.execute(delete(model).where(model.home_id == current_user.active_home_id))
        # Delete the user
        db.session.delete(current_user)
        db.session.commit()
        flash("User account has been deleted successfully", category="success")
        return render_template('auth/login.html')
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500