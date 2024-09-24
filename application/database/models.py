from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, Integer, DateTime, UniqueConstraint, and_, func, ForeignKey, select, text, event
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import inspect
from flask_login import UserMixin

from application.extension import db  

models = Blueprint('models', __name__)

@as_declarative()                       # Base class that all models will inherit from
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()     # Automatically sets the table name to the lowercase version of the class name

class ReprMixin:                        # Mixin class to add a generic __repr__ method to models
    def __repr__(self):
        cls = self.__class__                                                             # Get the class of the current instance
        attrs = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))             # Get all attributes of the class that are not methods
        fields = {a[0]: getattr(self, a[0]) for a in attrs if not(a[0].startswith('_'))} # Create a dictionary of attribute names and their values, excluding private attributes
        fields_str = ', '.join(f"{k}={v!r}" for k, v in fields.items())                  # Create a string representation of all the attributes
        return f"{cls.__name__}({fields_str})"                                           # Return a string formatted with the class name and the attributes
    
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    #email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    profile_picture_url: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # Define relationships
    abilities = relationship('UserAbility', back_populates="user", lazy='dynamic')
    preferences = relationship('UserPreference', back_populates="user", lazy='dynamic')
    homes = relationship('Home', back_populates="user", lazy='dynamic', foreign_keys='Home.user_id')
    photos = relationship('Photo', back_populates="user", lazy='dynamic')
    tasks = relationship('Task', back_populates="user", lazy='dynamic')
    supply = relationship('Supply', back_populates="user", lazy='dynamic')
    status = relationship('UserStatus', back_populates="user", lazy='dynamic')
    active_home_id: Mapped[int] = mapped_column(ForeignKey('home.id'), nullable=True)
    active_home = relationship("Home", foreign_keys=[active_home_id])
    custom = relationship('Custom', back_populates="user", lazy='dynamic')
    lists = relationship("UserList", back_populates="user", lazy='dynamic')



class UserList(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    list_type: Mapped[str] = mapped_column(String(50), nullable=False) # match model name
    list_name: Mapped[str] = mapped_column(String(80), nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'list_name', name='unique_list_name'),)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="lists")
    items = relationship("UserListEntry", back_populates="user_list", lazy='joined', cascade="all, delete-orphan") #bug test this


class UserListEntry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_list_id: Mapped[int] = mapped_column(ForeignKey('user_list.id'))
    item_model: Mapped[str] = mapped_column(String, nullable=False)  # Store the model name as a string
    item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    user_list = relationship("UserList", back_populates="items")

    __table_args__ = (
        UniqueConstraint('user_list_id', 'item_model', 'item_id', name='uq_user_list_item'),
    )
    def get_item(self):
        # Dynamically import the model
        model_class = globals()[self.item_model]
        return model_class.query.get(self.item_id) 
    #if model_class is Floor and you want the name of the floor: {{ item.get_item().floor_name }} 

class UserAbility(db.Model): # User's ability to do something, disabilities to account for
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    ability_type: Mapped[str]
    description: Mapped[str]
    user = relationship("User", back_populates="abilities")
    
class UserStatus(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    current_room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    focus: Mapped[str]
    mood: Mapped[str]
    energy_level: Mapped[int]
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    user = relationship("User", back_populates="status")
    
class UserPreference(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    measurement_unit: Mapped[str] = mapped_column(default='metric')
    notification_frequency: Mapped[str] = mapped_column(default='daily')
    theme: Mapped[str] = mapped_column(default='light')
    user = relationship("User", back_populates="preferences")

class Home(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    home_name: Mapped[str] = mapped_column(String(80), nullable=False)
    home_type: Mapped[str] = mapped_column(String(80), default='house')
    __table_args__ = (UniqueConstraint('user_id', 'home_name', name='unique_home_name'),)
    home_size_sqm: Mapped[float] = mapped_column(default=0.0)
    user = relationship("User", back_populates="homes", foreign_keys=[user_id])
    rooms = relationship('Room', back_populates="homes", lazy='dynamic', foreign_keys="[Room.home_id]")
    floors = relationship('Floor', back_populates="homes", lazy='dynamic', foreign_keys='Floor.home_id')
    last_full_walkthrough: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    active_floor_id: Mapped[int] = mapped_column(ForeignKey('floor.id'), nullable=True)
    active_floor = relationship("Floor", foreign_keys=[active_floor_id])
    ground_floor_id: Mapped[int] = mapped_column(ForeignKey('floor.id'), nullable=True)
    ground_floor = relationship("Floor", foreign_keys=[ground_floor_id])
    active_room_id: Mapped[int] = mapped_column(ForeignKey('room.id'), nullable=True)
    active_room = relationship("Room", foreign_keys=[active_room_id])
    
    def get_floor_count(self):
        return self.floors.count()
    def get_room_count(self):
        return self.rooms.count()



class Floor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    home_id: Mapped[int] = mapped_column(ForeignKey('home.id'))
    floor_name: Mapped[str] = mapped_column(String(80), nullable=False)
    homes = relationship('Home', back_populates="floors", foreign_keys=[home_id])
    rooms = relationship('Room', back_populates="floors")

    @property
    def as_list_item(self):
        return {
            'id': self.id,
            'type': 'floor',
            'name': self.floor_name,
            'additional_info': f"Home: {self.home.home_name}"
        }
    

class Room(db.Model): #[ ]: ROOM LEVEL AND LOCATION ON THE MAP
    id: Mapped[int] = mapped_column(primary_key=True)
    home_id: Mapped[int] = mapped_column(ForeignKey('home.id'))
    floor_id: Mapped[int] = mapped_column(ForeignKey('floor.id'))
    room_type: Mapped[str] = mapped_column(default='Room')
    @property
    def same_type_rooms_count(self):
        return db.session.execute(
            select(db.func.count())
            .select_from(Room.__table__)
            .where(and_(Room.home_id == self.home_id, Room.room_type == self.room_type))
        ).scalar()
    
    room_name: Mapped[str] = mapped_column(
        default=text("f'{room_type}' || ({same_type_rooms_count} + 1)")
    ) # find room types and add 1 to the count and use that as the default room name
    #room_size: Mapped[float] = mapped_column(default=0.0)
    #room_function: Mapped[str] = mapped_column(default='')
    #room_frequency_of_use: Mapped[str] = mapped_column(default='')
    #room_importance: Mapped[str] = mapped_column(default='')
    #room_dirtiness_level: Mapped[float] = mapped_column(default=0.0)
    #room_tools_supplies_on_hand: Mapped[str] = mapped_column(default='')
    #room_tools_supplies_required: Mapped[str] = mapped_column(default='')
    homes = relationship("Home", back_populates="rooms", foreign_keys=[home_id])
    floors = relationship("Floor", back_populates="rooms", foreign_keys=[floor_id])
    zones = relationship('Zone', back_populates="rooms", lazy='dynamic')
    supply = relationship('Supply', back_populates="rooms", lazy='dynamic')
    @property
    def as_list_item(self):
        return {
            'id': self.id,
            'type': 'room',
            'name': self.room_name,
            'additional_info': f"Floor: {self.floors.floor_name}"
        }
    
class Custom(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    category: Mapped[str]
    title: Mapped[str]
    user = relationship("User", back_populates="custom")
    
    

class Zone(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    surface_type: Mapped[str]
    usage_frequency: Mapped[str]
    importance: Mapped[int]
    dirtiness_score: Mapped[int]
    effort_required: Mapped[int]
    rooms = relationship('Room', back_populates="zones")
    appliances = relationship('Appliance', back_populates="zones", lazy='dynamic')
    
class Appliance(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    zone_id: Mapped[int] = mapped_column(ForeignKey('zone.id'))
    appliance: Mapped[str]
    zones = relationship('Zone', back_populates="appliances")
    
class Photo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    photo_url: Mapped[str]
    is_before_photo: Mapped[bool]
    photo_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    user = relationship("User", back_populates="photos")
    annotations = relationship('TaskAnnotation', back_populates="photos", lazy='dynamic')

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    task_title: Mapped[str] = mapped_column(default=text("'Task #' || (last_insert_rowid() + 1)"))
    task_description: Mapped[str] = mapped_column(nullable=True)
    task_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    task_updated_at: Mapped[datetime] = mapped_column('task_updated_at', DateTime(timezone=True), default=func.now())
    task_due_date: Mapped[datetime] = mapped_column(nullable=True)
    task_priority: Mapped[int] = mapped_column(nullable=True)
    task_status: Mapped[str] = mapped_column(nullable=True)
    task_tags: Mapped[str] = mapped_column(nullable=True)
    task_scheduled_time: Mapped[datetime] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    user = relationship("User", back_populates="tasks")
    progress = relationship('TaskProgress', back_populates="tasks")
    annotations = relationship("TaskAnnotation", back_populates="tasks")
    @property
    def as_list_item(self):
        return {
            'id': self.id,
            'type': 'task',
            'name': self.task_title,
            'additional_info': f"Due: {self.task_due_date.strftime('%Y-%m-%d') if self.task_due_date else 'Not set'}"
        }
    
    @hybrid_property
    def task_updated_at(self):
        return self._task_updated_at

    @task_updated_at.setter
    def task_updated_at(self, value):
        self._task_updated_at = value

@event.listens_for(Task, 'before_update')
def receive_before_update(mapper, connection, target):
    target.task_updated_at = func.now()

class TaskAnnotation(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'))
    photo_id: Mapped[int] = mapped_column(ForeignKey('photo.id'))
    x_coordinate: Mapped[float]
    y_coordinate: Mapped[float]
    annotation_text: Mapped[str]
    photos = relationship('Photo', back_populates="annotations")
    tasks = relationship('Task', back_populates="annotations")

class TaskProgress(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'))
    progress_photo_url: Mapped[str]
    progress_timestamp: Mapped[datetime]
    progress_description: Mapped[str]
    completion_percentage: Mapped[float]
    tasks = relationship('Task', back_populates="progress")
    
'''class TaskCompletionHistory(db.Model):
    completion_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    after_photo_url: Mapped[str]'''
    
'''class SharedTask(db.Model):
    share_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    shared_with: Mapped[str]
    share_timestamp: Mapped[datetime]
    comments: Mapped[str]
    likes: Mapped[int]
    feedback: Mapped[str]'''

'''class Notification(db.Model):
    notification_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    notification_message: Mapped[str]
    notification_status: Mapped[str]
    reminder_time: Mapped[datetime]'''

class Supply(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id')) #room where the item is stored
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    item_name: Mapped[str]
    item_type: Mapped[str]
    quantity: Mapped[int]
    rooms = relationship('Room', back_populates="supply")
    user = relationship("User", back_populates="supply")
    @property
    def as_list_item(self):
        return {
            'id': self.id,
            'type': 'supply',
            'name': self.item_name,
            'additional_info': f"Quantity: {self.quantity}"
        }

'''class UserSchedule(db.Model):
    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    event_name: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]'''

'''class ProductRecommendation(db.Model):
    recommendation_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    product_name: Mapped[str]
    product_url: Mapped[str]
    price: Mapped[float]

class ServiceRecommendation(db.Model):
    recommendation_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    service_name: Mapped[str]
    service_url: Mapped[str]
    price: Mapped[float]'''