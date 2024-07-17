from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import as_declarative
import inspect

db = SQLAlchemy()

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
    
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    profile_picture_url: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class UserAbility(db.Model):
    ability_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    ability_type: Mapped[str]
    description: Mapped[str]

class UserPreference(db.Model):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), primary_key=True)
    measurement_unit: Mapped[str] = mapped_column(default='metric')
    notification_frequency: Mapped[str] = mapped_column(default='daily')
    theme: Mapped[str] = mapped_column(default='light')

class Home(db.Model):
    home_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    home_size_sqm: Mapped[float]
    num_floors: Mapped[int]
    layout: Mapped[str]

class Room(db.Model):
    room_id: Mapped[int] = mapped_column(primary_key=True)
    home_id: Mapped[int] = mapped_column(ForeignKey('home.home_id'))
    room_name: Mapped[str]
    room_type: Mapped[str]
    room_size: Mapped[float]
    room_flooring_type: Mapped[str]
    room_windows: Mapped[int]
    room_function: Mapped[str]
    room_frequency_of_use: Mapped[str]
    room_importance: Mapped[str]
    room_dirtiness_level: Mapped[float]
    room_tools_supplies_on_hand: Mapped[str]
    room_tools_supplies_required: Mapped[str]

class RoomDetail(db.Model):
    detail_id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    appliance: Mapped[str]
    surface_type: Mapped[str]
    usage_frequency: Mapped[str]
    importance: Mapped[int]
    aesthetic_score: Mapped[int]
    dirtiness_score: Mapped[int]
    effort_required: Mapped[int]

class Photo(db.Model):
    photo_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    photo_url: Mapped[str]
    is_before_photo: Mapped[bool]
    photo_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Task(db.Model):
    task_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    task_title: Mapped[str]
    task_description: Mapped[str]
    task_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    task_due_time: Mapped[datetime]
    task_priority: Mapped[int]
    task_status: Mapped[str]
    task_tags: Mapped[str]
    task_scheduled_time: Mapped[datetime]
    task_type: Mapped[str]
    completed_at: Mapped[Optional[datetime]]

class TaskAnnotation(db.Model):
    annotation_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    x_coordinate: Mapped[float]
    y_coordinate: Mapped[float]
    annotation_text: Mapped[str]

class TaskProgress(db.Model):
    progress_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    progress_photo_url: Mapped[str]
    progress_timestamp: Mapped[datetime]
    progress_description: Mapped[str]
    completion_percentage: Mapped[float]

class SharedTask(db.Model):
    share_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    shared_with: Mapped[str]
    share_timestamp: Mapped[datetime]
    comments: Mapped[str]
    likes: Mapped[int]
    feedback: Mapped[str]

class Notification(db.Model):
    notification_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    notification_message: Mapped[str]
    notification_status: Mapped[str]
    reminder_time: Mapped[datetime]

class ToolSupply(db.Model):
    item_id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    item_name: Mapped[str]
    item_type: Mapped[str]
    is_on_hand: Mapped[bool]

class UserStatus(db.Model):
    status_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    current_room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    focus: Mapped[str]
    mood: Mapped[str]
    energy_level: Mapped[int]
    last_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class UserSchedule(db.Model):
    schedule_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    event_name: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

class ProductRecommendation(db.Model):
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
    price: Mapped[float]

class TaskCompletionHistory(db.Model):
    completion_id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.task_id'))
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    after_photo_url: Mapped[str]