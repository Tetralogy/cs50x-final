from typing import List, Optional

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from application.database.models import Floor, Room, Supply, Task, UserList, UserListItem
from application.extension import db

    
lists = Blueprint('lists', __name__)

# Helper functions for CRUD operations
def create_user_list(list_type: str, list_name: str) -> UserList:
    if not list_type or not list_name:
        raise ValueError('All arguments are required')
    model_class = globals().get(list_type)
    if not model_class or not issubclass(model_class, db.Model) and list_type != 'Mixed':
        raise ValueError(f'Unknown list type {list_type}')
    existing_list = db.session.execute(
        select(UserList).filter_by(user_id=current_user.id, list_name=list_name)
    ).scalar()
    if existing_list:
        return existing_list
    new_list = UserList(user_id=current_user.id, list_name=list_name, list_type=list_type)
    db.session.add(new_list)
    db.session.commit()
    return new_list

def add_item_to_list(user_list_id: int, item_model: str, item_id: int = None, order: int = None) -> UserListItem:
    list_obj = db.get_or_404(UserList, user_list_id)
    if not list_obj:
        raise ValueError(f'Unknown list id {user_list_id}')
    if item_model is None:
        raise ValueError('item_model cannot be None')
    model_class = globals().get(item_model)
    if not model_class or not issubclass(model_class, db.Model):
        raise ValueError(f'Unknown item type {item_model}')
    if item_id is None:
        new_item = create_new_default(item_model) #FIXME: TEST THIS WITH CREATE NEW FLOOR
        item_id = new_item.item_id
    if order is None:
        order = db.session.scalars(db.select(db.func.count()).select_from(UserListItem).where(UserListItem.user_list_id == user_list_id)).one()
    new_list_item = UserListItem(user_list_id=user_list_id, item_model=item_model, item_id=item_id, order=order)
    db.session.add(new_list_item)
    db.session.commit()
    return new_list_item

def create_new_default(item_model: str) -> UserListItem:
    if item_model == 'Floor':
        current_home = current_user.active_home
        floor_name = set_default_floor_name()
        new_item = Floor(home_id=current_home.id, floor_name=floor_name) #creates default floor #FIXME: TEST THIS WITH CREATE NEW FLOOR
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(item_model=item_model, item_id=new_item.id)
    if item_model == 'Task':
        new_item = Task(user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(item_model=item_model, item_id=new_item.id)
    if item_model == 'Room':
        new_item = Room(home_id=current_user.active_home.id, floor_id=current_user.active_home.active_floor.id)
        db.session.add(new_item)
        db.session.commit()
        return UserListItem(item_model=item_model, item_id=new_item.id)
    else:
        raise ValueError(f'Unknown item type {item_model}')
'''
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
'''
def get_list_id(item_model: str):
    list_type = item_model
    lists = current_user.lists.filter_by(list_type=list_type).all()
    if len(lists) == 0:
        raise ValueError(f'No lists of type {list_type} found for user {current_user.id}')
    if len(lists) > 1:
        print('More than one list matches the string. Please select one:')
        for i, lst in enumerate(lists):
            print(f'{i+1}. {lst.list_name}')
        selected_list_index = int(input('Enter the number of the list: '))
        list_id = lists[selected_list_index-1].id
    else:
        list_id = lists[0].id
    if not isinstance(list_id, int):
        if isinstance(list_id, str):
            list_type = list_id
            lists = current_user.lists.filter_by(list_type=list_type).all()
            if len(lists) == 0:
                raise ValueError(f'No lists of type {list_type} found for user {current_user.id}')
            if len(lists) > 1:
                print('More than one list matches the string. Please select one:')
                for i, lst in enumerate(lists):
                    print(f'{i+1}. {lst.list_name}')
                selected_list_index = int(input('Enter the number of the list: '))
                list_id = lists[selected_list_index-1].id
            else:
                list_id = lists[0].id
    return list_id

def update_item_order(user_list_item_id: int, new_order: int) -> Optional[UserListItem]:
    item = UserListItem.query.get(user_list_item_id)
    if item:
        item.order = new_order
        db.session.commit()
        return item
    return None

def delete_item_from_list(user_list_item_id: int) -> bool:
    item = db.get_or_404(UserListItem, user_list_item_id)
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

def set_default_floor_name():
    floor_count = current_user.active_home.floors.count()
    print(f'floor_count: {floor_count}')
    if floor_count == 0:
        return "Main Floor"
    if floor_count == 1:
        suffix = "nd"
    elif floor_count == 2:
        suffix = "rd"
    else:
        suffix = "th"
    return f"{floor_count}{suffix} Floor"


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

@lists.route('/show_list/<int:list_id>', methods=['GET'])
@login_required
def show_list(list_id):
    return render_template('lists/list.html.jinja', list_obj=db.get_or_404(UserList, list_id)) #bug: fix template

@lists.route('/update_list_order/<int:list_id>', methods=['PUT'])
@login_required
def update_list_order(list_id):
    order = request.form.getlist('order')
    for index, item_id in enumerate(order):
        update_item_order(item_id, index)
    flash('List order updated')
    return redirect(url_for('lists.get_list', list_id=list_id))


