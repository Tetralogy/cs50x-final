from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from .models import User, Home, Room, Photo, Task, Pin

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

'''class UserAbilitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserAbility
        include_relationships = True
        load_instance = True'''

'''class UserStatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserStatus
        include_relationships = True
        load_instance = True

class UserPreferenceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserPreference
        include_relationships = True
        load_instance = True'''

class HomeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Home
        include_relationships = True
        load_instance = True

class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_relationships = True
        load_instance = True

'''class ZoneSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Zone
        include_relationships = True
        load_instance = True

class ApplianceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appliance
        include_relationships = True
        load_instance = True'''

class PhotoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Photo
        include_relationships = True
        load_instance = True

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

class PinSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pin
        include_relationships = True
        load_instance = True
        

'''class TaskProgressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TaskProgress
        include_relationships = True
        load_instance = True

class SupplySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Supply
        include_relationships = True
        load_instance = True'''

# Create instances of each schema
user_schema = UserSchema()
'''user_ability_schema = UserAbilitySchema()
user_status_schema = UserStatusSchema()
user_preference_schema = UserPreferenceSchema()'''
home_schema = HomeSchema()
room_schema = RoomSchema()
'''zone_schema = ZoneSchema()
appliance_schema = ApplianceSchema()'''
photo_schema = PhotoSchema()
task_schema = TaskSchema()
pin_schema = PinSchema()
'''task_progress_schema = TaskProgressSchema()
supply_schema = SupplySchema()'''

# Create instances for handling multiple objects
users_schema = UserSchema(many=True)
tasks_schema = TaskSchema(many=True)
# ... create similar instances for other models as needed