from typing import List, Optional

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from application.database.models import Floor, Room, Supply, Task, UserList, UserListItem
from application.extension import db
    
lists = Blueprint('lists', __name__)

# Helper functions for CRUD operations
def create_user_list(user_id: int, list_name: str, list_type: str) -> UserList:
    new_list = UserList(user_id=user_id, list_name=list_name, list_type=list_type)
    db.session.add(new_list)
    db.session.commit()
    return new_list

def create_new_default(item_model: str) -> UserListItem:
    if item_model == 'Floor':
        new_item = Floor(home_id=current_user.active_home.id) #creates default floor
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(item_model=item_model, item_id=new_item.id)
    if item_model == 'Task':
        new_item = Task(user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(item_model=item_model, item_id=new_item.id)
    if item_model == 'Room':
        new_item = Room(home_id=current_user.active_home.id, floor_id=current_user.active_home.active_floor.id, order=0, room_name=item_model, room_type='')
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(user_list_id=current_user.active_list_id, item_model=item_model, item_id=new_item.id, order=0)
    else:
        raise ValueError(f'Unknown item type {item_model}')
    return new_item
def add_item_to_list(user_list_id: int, item_model: str, item_id: int, order: int) -> UserListItem:
    item_id: Optional[int] = None, order: Optional[int] = None
    if item_id is None:
        new_item = create_new_default(item_model)
        new_item = item_model(name=f'{item_model} ', home_id=current_user.active_home.id)
        '''if item_model == 'room':
            item = Room(name=item_model, home_id=current_user.active_home.id)
        elif item_model == 'task':
            item = Task(name=item_model, room_id=current_user.active_home.active_room.id)
        elif item_model == 'supply':
            item = Supply(name=item_model, room_id=current_user.active_home.active_room.id)
        else:
            raise ValueError(f'Unknown item type {item_model}')'''
        db.session.add(item)
        db.session.commit()
        item_id = item.id
    if order is None:
        order = UserListItem.query.filter_by(user_list_id=user_list_id).count()
    new_item = UserListItem(user_list_id=user_list_id, item_model=item_model, item_id=item_id, order=order)
    db.session.add(new_item)
    db.session.commit()
    return new_item

def get_user_list_items(user_list_id: int) -> List[dict]:
    items = UserListItem.query.filter_by(user_list_id=user_list_id).order_by(UserListItem.order).all()
    result = []
    for item in items:
        if item.item_type == 'room':
            obj = Room.query.get(item.item_id)
        elif item.item_type == 'task':
            obj = Task.query.get(item.item_id)
        elif item.item_type == 'supply':
            obj = Supply.query.get(item.item_id)
        else:
            # Handle custom items
            obj = {'id': item.item_id, 'type': item.item_type, 'name': 'Custom Item', 'additional_info': item.custom_data}
        
        list_item = obj.as_list_item if hasattr(obj, 'as_list_item') else obj
        list_item['order'] = item.order
        list_item['custom_data'] = item.custom_data
        result.listsend(list_item)
    return result

def update_item_order(user_list_item_id: int, new_order: int) -> Optional[UserListItem]:
    item = UserListItem.query.get(user_list_item_id)
    if item:
        item.order = new_order
        db.session.commit()
        return item
    return None

def delete_item_from_list(user_list_item_id: int) -> bool:
    item = UserListItem.query.get(user_list_item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False

def add_custom_item_to_list(user_list_id: int, name: str, order: int, custom_data: str = None) -> UserListItem:
    new_item = UserListItem(user_list_id=user_list_id, item_type='custom', item_id=0, order=order, custom_data=custom_data)
    db.session.add(new_item)
    db.session.commit()
    return new_item

# Example usage in a Flask route
@lists.route('/create_list', methods=['POST'])
@login_required
def create_list():
    list_name = request.form.get('list_name')
    list_type = request.form.get('list_type', 'custom')
    new_list = create_user_list(current_user.id, list_name, list_type)
    flash(f'List created: {new_list.list_name}')
    return redirect(url_for('lists.get_list', list_id=new_list.id))

@lists.route('/add_to_list/<int:list_id>', methods=['POST'])
@login_required
def add_to_list(list_id):
    item_model = request.form.get('item_model')
    item_id = request.form.get('item_id')
    order = request.form.get('order')
    
    if item_model == 'custom':
        new_item = add_custom_item_to_list(list_id, item_id, order)
    else:
        new_item = add_item_to_list(list_id, item_model, item_id, order)
    
    flash(f'Item added to list: {new_item.item_model} {new_item.item_id}')
    return redirect(url_for('lists.get_list', list_id=list_id))

@lists.route('/get_list/<int:list_id>', methods=['GET'])
@login_required
def get_list(list_id):
    items = get_user_list_items(list_id)
    return render_template('list.html', items=items, list_id=list_id)

@lists.route('/update_list_order/<int:list_id>', methods=['PUT'])
@login_required
def update_list_order(list_id):
    order = request.form.getlist('order')
    for index, item_id in enumerate(order):
        update_item_order(item_id, index)
    flash('List order updated')
    return redirect(url_for('lists.get_list', list_id=list_id))


