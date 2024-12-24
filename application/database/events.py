from datetime import datetime
import logging
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property, attributes, object_session
from sqlalchemy import Boolean, String, Integer, DateTime, UniqueConstraint, and_, delete, func, ForeignKey, select, text, event, Enum

from application.database.models import Home, Photo, Pin, Room, Task, TaskStatus, User, UserListEntry
from application.list_utils import get_userlist
from application.extension import db
from logs.logging_config import ApplicationLogger

logger = ApplicationLogger.get_logger(__name__)

'''
@event.listens_for(Room, 'before_update')
def duplicate_pins_for_new_cover_photo(mapper, connection, target):
    logger.debug(f'duplicate_pins_for_new_cover_photo called for room: {target}')
    # Check if current_cover_photo_id has actually changed
    if attributes.get_history(target, 'current_cover_photo_id').has_changes():
        # Get the previous value of current_cover_photo_id
        previous_cover_photo_id = attributes.get_history(target, 'current_cover_photo_id').deleted[0]
        # Find all pins associated with the previous cover photo
        pins_to_duplicate = db.session.query(Pin).filter(Pin.photo_id == previous_cover_photo_id).all()
        # Create new pins for the new cover photo
        for original_pin in pins_to_duplicate:
            # Create a new pin with the same attributes, but with the new photo ID
            new_pin = Pin(
                # Copy all attributes from the original pin
                **{
                    col.name: getattr(original_pin, col.name) 
                    for col in Pin.__table__.columns 
                    if col.name != 'id' and col.name != 'photo_id'
                },
                # Set the new photo ID
                photo_id=target.current_cover_photo_id
            )
            # Add the new pin to the session
            db.session.add(new_pin)
            found_pin_entry = UserListEntry.find_entries_for_item(original_pin)[0]
            #get the userlist for the new cover photo to attach the duplicate pin entries
            found_photo_entry = UserListEntry.find_entries_for_item(target.current_cover_photo_id)[0],
            new_pin_entry = UserListEntry(
                # Copy all attributes from the original entry
                **{
                    col.name: getattr(found_pin_entry, col.name) 
                    for col in UserListEntry.__table__.columns 
                    if col.name != 'id' and col.name != 'user_list_id' and col.name != 'item_id'
                },
                # Set the new userlist ID
                user_list_id = get_userlist(item_model='Pin', parent_entry_id=found_photo_entry).id,
                item_id = new_pin.id
            )
            # Add the new entry to the session
            db.session.add(new_pin_entry)
        # Set the new cover photo to is_cover_photo=True
        db.execute(
            Photo.__table__.update().where(Photo.id == target.current_cover_photo_id).values(is_cover_photo=True)
        )
        logger.debug(f'duplicate_pins_for_new_cover_photo called for room: {target}')
        # Commit the new pins
        db.session.commit()
        '''

@event.listens_for(Pin, 'before_insert')
def remove_old_pin_and_entry_if_duplicate_task_on_photo(mapper, connection, target):
    # check for matching pins
    old_pin_query = select(Pin).where(
        Pin.task_id == target.task_id, 
        Pin.photo_id == target.photo_id,
        Pin.id != target.id  # Ensure it is a different pin
        ).limit(1)
    old_pin = db.session.execute(old_pin_query).scalars().first()
    logger.debug(f'remove_old_pin_and_entry_if_duplicate_task_on_photo called for pin: {target}')
    logger.debug(f'old_pin1: {old_pin}')
    if old_pin:
        logger.debug(f'old_pin2: {old_pin}')
        # Delete the old entry
        db.session.execute(delete(UserListEntry).where(UserListEntry.item_id == old_pin.id))
        # Delete the old pin
        db.session.delete(old_pin)
        logger.debug(f'old_pin3: {old_pin}')
        #db.session.commit()
    else:
        logger.debug("No matching pin found, nothing to delete.")
        
@event.listens_for(Task, 'before_update')
def set_timestamp_on_completion(mapper, connection, target):
    target.last_updated_at = func.now()
    
    # Check if the status is being set to COMPLETED
    if target.status == TaskStatus.COMPLETED and target.completed_at is None:
        target.completed_at = datetime.now()
    logger.info(f'set_timestamp_on_completion called for task: {target}')
    
@event.listens_for(Home, 'before_update')
def update_active_floor(mapper, connection, target):
    session = object_session(target)
    active_room_id_history = attributes.get_history(target, 'active_room_id')
    # Check if the active_room_id has changed
    if active_room_id_history.has_changes():
        if target.active_room_id is not None:
            room = session.query(Room).get(target.active_room_id)
            target.active_floor_id = room.floor_id
            

@event.listens_for(Room, 'before_delete')
def clear_active_room_id(mapper, connection, target):
    session = object_session(target)
    home = session.query(Home).get(target.home_id)
    if home and home.active_room_id == target.id:
        home.active_room_id = None
        session.add(home)
        
@event.listens_for(User, 'before_update')
def debug_reset_tutorials(mapper, connection, target):
    if target.debug == True:
        target.tutorial_pingrid_dismissed = False
        target.tutorial_floors_dismissed = False
        target.tutorial_rooms_dismissed = False
        target.tutorial_home_dismissed = False