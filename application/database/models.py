from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username!r}, email={self.email!r})"
    
'''
    #TODO #1 organize the tables
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional, List

db = SQLAlchemy()

#todo #2 test the issues workflow

class User(db.Model):
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    profile_picture_url: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_login: Mapped[Optional[datetime]]

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
    photo_timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Task(db.Model):
    task_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('room.room_id'))
    task_title: Mapped[str]
    task_description: Mapped[str]
    task_created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
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
    last_updated: Mapped[datetime] = mapped_column(default=datetime.utcnow)

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
    completed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    after_photo_url: Mapped[str]

    '''