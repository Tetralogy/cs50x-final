from typing import List, Optional

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from application.database.models import Floor, Room, Supply, Task, UserList, UserListEntry
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

def add_item_to_list(user_list_id: int, item_model: str, item_id: int = None, order: int = None, name: str = None) -> UserListEntry:
    list_obj = db.get_or_404(UserList, user_list_id)
    if not list_obj:
        raise ValueError(f'Unknown list id {user_list_id}')
    if item_model is None:
        raise ValueError('item_model cannot be None')
    model_class = globals().get(item_model)
    if not model_class or not issubclass(model_class, db.Model):
        raise ValueError(f'Unknown item type {item_model}')
    if item_id is None:
        new_item = create_new_default(item_model, name) 
        item_id = new_item.item_id
    if order is None:
        order = db.session.scalars(db.select(db.func.count()).select_from(UserListEntry).where(UserListEntry.user_list_id == user_list_id)).one()
    elif order < 1:
        all_items = db.session.scalars(db.select(UserListEntry).filter_by(user_list_id=user_list_id).order_by(UserListEntry.order)).all()
        for item in all_items:            
            item.order += 1
        db.session.commit()
        order = 0
    new_list_item = UserListEntry(user_list_id=user_list_id, item_model=item_model, item_id=item_id, order=order)
    db.session.add(new_list_item)
    db.session.commit()
    return new_list_item

def create_new_default(item_model: str, name: str = None) -> UserListEntry:
    if item_model == 'Floor':
        print(f'name (create_new_default):  {name}')
        current_home = current_user.active_home
        if name is None:
            floor_name = set_default_floor_name()
        else:
            count = 0
            existing_floors = db.session.scalars(db.select(Floor.floor_name).filter(Floor.home_id == current_home.id)).all()
            for floor_name in existing_floors:
                if name in floor_name:
                    count += 1
                floor_name = f'{name} {count + 1}'
                print(f'floor_name (create_new_default): {floor_name}')
        new_item = Floor(home_id=current_home.id, floor_name=floor_name) #creates default floor
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Task':
        new_item = Task(user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Room':
        new_item = Room(home_id=current_user.active_home.id, floor_id=current_user.active_home.active_floor.id)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
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
def get_userlist(item_model: str): #gets the primary list of a main model
    list_type = item_model
    lists = current_user.lists.filter_by(list_type=list_type).all()
    if len(lists) == 0:
        raise ValueError(f'No lists of type {list_type} found for user {current_user.id}')
    if len(lists) > 1: #[ ] add ability to select which list when more than one + test this
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
    userlist =  db.get_or_404(UserList, list_id)
    return userlist

def update_item_order(user_list_entry_id: int, new_order: int) -> Optional[UserListEntry]:
    item = db.session.scalars(db.select(UserListEntry).filter_by(id=user_list_entry_id)).one_or_none()
    if item:
        item.order = new_order
        db.session.commit()
        return item
    return None

def delete_entry_and_item(user_list_entry_id: int) -> bool:
    userlist_entry = db.get_or_404(UserListEntry, user_list_entry_id)
    
    if userlist_entry:
        item = userlist_entry.get_item()  # Use the get_item method to fetch the item
        if item is None:
            print('Item to delete not found')
            return False, 404
        db.session.delete(item)
        db.session.delete(userlist_entry)
        db.session.commit()
        return True
    return False

def add_custom_item_to_list(user_list_id: int, name: str, order: int, custom_data: str = None) -> UserListEntry:
    new_item = UserListEntry(user_list_id=user_list_id, item_type='custom', item_id=0, order=order, custom_data=custom_data)
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
    return f"{floor_count + 1}{suffix} Floor"


# Example usage in a Flask route
@lists.route('/create_list', methods=['POST'])
@login_required
def create_list():
    list_name = request.form.get('list_name')
    list_type = request.form.get('list_type', 'custom')
    new_list = create_user_list(current_user.id, list_name, list_type)
    flash(f'List created: {new_list.list_name}')
    return redirect(url_for('lists.get_list', list_id=new_list.id))

'''@lists.route('/add_to_list/<int:list_id>', methods=['POST'])
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
    return redirect(url_for('lists.get_list', list_id=list_id))'''
@lists.route('/create/<string:item_model>/<int:list_id>', methods=['POST'])
@login_required
def create_add_to_list(item_model, list_id, item_id=None):
    order = request.args.get('order')
    if order is None or order == '':
        order = None
    else:
        order = int(order)
    name = request.args.get('name')
    print(f'item_model: {item_model}, list_id: {list_id}, item_id: {item_id}, order: {order}, name: {name}')
    new_item = add_item_to_list(list_id, item_model, item_id, order, name)
    
    flash(f'Item added to list: {new_item.item_model} {new_item.item_id}')
    return redirect(url_for('lists.update_list_order', list_id=list_id))

@lists.route('/delete/<int:list_id>/<int:user_list_entry_id>', methods=['DELETE'])
@login_required
def delete(list_id, user_list_entry_id):
    if delete_entry_and_item(user_list_entry_id):
        flash(f'list_id: {list_id} user_list_entry_id: {user_list_entry_id} Item deleted')
    else:
        flash('Item not found', 'error')
    return redirect(url_for('lists.update_list_order', list_id=list_id))

@lists.route('/update_list_order/<int:list_id>', methods=['PUT', 'POST', 'DELETE', 'GET'])
@login_required
def update_list_order(list_id):
    order = request.form.getlist('order')
    print(f'list_id: {list_id}, order1: {order}')
    if order is None or len(order) == 0:
        userlist = db.get_or_404(UserList, list_id)
        order = db.session.scalars(select(UserListEntry).filter_by(user_list_id=userlist.id).order_by(UserListEntry.order)).all()
        print(f'UserList {userlist.list_name} order2: {order}')

    # Extract the IDs if they are UserListEntry objects
    if hasattr(order[0], 'id'):
        order = [entry.id for entry in order]
            
    for index, item_id in enumerate(order):
        print(f'Updating item_id: {item_id} with new order: {index}')
        update_item_order(item_id, index)
    flash('List order updated')
    return redirect(url_for('lists.show_list', list_id=list_id))

@lists.route('/show_list/<int:list_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def show_list(list_id):
    print(f'showing list list_id: {list_id}')
    return render_template('lists/list.html.jinja', list_obj=db.get_or_404(UserList, list_id))


@lists.route('/rename/<string:item_model>/<int:item_id>', methods=['PUT'])
@login_required
def rename_item(item_model, item_id):
    new_name = request.form.get('input_name')
    print(f'renaming item_model: {item_model}, item_id: {item_id} to {new_name}')
    print(request.form)
    if item_model == 'room':
        room = db.get_or_404(Room, item_id)
        room.floor_name = new_name
    elif item_model == 'task':
        task = db.get_or_404(Task, item_id)
        task.name = new_name
    elif item_model == 'supply':
        supply = db.get_or_404(Supply, item_id)
        supply.name = new_name
    db.session.commit()
    return '', 204
