import logging
import os
import time
from sqlalchemy import select
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, session, url_for
from flask_login import current_user, login_required

from application.database.models import Photo, Room, Task, UserList, UserListEntry
from application.list_utils import add_item_to_list, create_user_list, default_list_name, delete_entry_and_item, get_immediate_child_lists, get_list_entries_for_item, get_top_userlists_by_root_parent, get_userlist, get_userlists_by_parent, update_entry_order
from application.extension import db
from logs.logging_config import ApplicationLogger

lists = Blueprint('lists', __name__)
logger = ApplicationLogger.get_logger(__name__)

@lists.route('/create/<string:item_model>', methods=['POST'])
@login_required
def create_list_and_item_and_entry(item_model, retrieve: str=None):
    if item_model == 'Home':
        multifloor=request.form.get('multifloor') == 'on'
        #logger.debug(f'multifloor: {multifloor}')
        list_name = f'{current_user.username} {item_model}s'
        userlist = get_userlist(item_model, list_name)
        if not userlist:
            userlist = create_user_list(item_model, list_name)
        name = request.form.get('name_input')
        new_home_entry = add_item_to_list(userlist.id, item_model, name=name)
        current_user.active_home_id = new_home_entry.item_id
        db.session.commit()
        if multifloor:
            #logger.debug(f'multifloor check: {multifloor}')
            return redirect(url_for('floors.define_floors', multifloor=multifloor))
        return redirect(url_for('homes.home_setup'))
    if item_model == 'Floor':
        parent_entry_id = get_list_entries_for_item(current_user.active_home)[0].id
        list_name = f'{current_user.active_home.name} {item_model}s'
        userlist = get_userlist(item_model, list_name, parent_entry_id)
        if not userlist:
            userlist = create_user_list(item_model, list_name, parent_entry_id)
        name = request.form.get('name') # check if basement or not
        order_index = request.form.get('order_index')
        if not order_index:
            order_index = None
        else:
            order_index = int(order_index)
        item_id = None
        #logger.debug(f'item_model: {item_model}, list_id: {userlist.id}, item_id: {item_id}, order: {order_index}, name: {name}')
        new_item = add_item_to_list(userlist.id, item_model, item_id, order_index, name)
        flash(f'Item added to list: {new_item.item_model} {new_item.item_id}', 'success')
        return render_template('lists/model/' + new_item.item_model.lower() + '.html.jinja', entry=new_item)
    room_id = request.form.get('room_id')
    list_name, parent_entry_id = default_list_name(item_model=item_model, room_id=room_id)
    userlist = get_userlist(item_model, list_name, parent_entry_id) 
    if not userlist:
        userlist = create_user_list(item_model, list_name, parent_entry_id)
    return create_item_and_entry(item_model, userlist.id, retrieve=retrieve)
    #return redirect(url_for('lists.create_item_and_entry', item_model=item_model, list_id=userlist.id))
    
@lists.route('/create/<string:item_model>/<int:list_id>', methods=['POST'])
@login_required
def create_item_and_entry(item_model, list_id, item_id: int=None, retrieve: str=None, task_id: int=None):
    order_index = request.form.get('order_index')
    if not order_index:
        order_index = None
    else:
        order_index = int(order_index)
    name = request.form.get('name')
    from_model = request.form.get('from_model')
    logger.debug(f'create_item_and_entry(): item_model: {item_model}, list_id: {list_id}, item_id: {item_id}, order: {order_index}, name: {name}')
    if from_model == 'Task':
        task_id = request.form.get('task_id')
        task = db.get_or_404(Task, task_id)
    new_item = add_item_to_list(list_id, item_model, item_id, order_index, name, task_id=task_id)
    if retrieve == 'list':
        userlist = db.get_or_404(UserList, list_id)
        logger.debug(f'retrieve: {retrieve}')
        return userlist
    if not new_item:
        logger.debug(f'Item NOT added to list: {item_model} {item_id}')
        return None, 404
    logger.debug(f'Item added to list: {new_item.item_model} entry {new_item.item_id}')
    #return 'test', 200
    #return render_template('lists/model/pin.html.jinja', entry=new_item)
    return render_template('lists/model/' + new_item.item_model.lower() + '.html.jinja', entry=new_item, child_lists=None) #redirect(url_for('lists.update_list_order', list_id=list_id))


@lists.route('/move_entry/', methods=['PUT'])
@lists.route('/move_entry/<int:moved_entry_id>', methods=['PUT'])
@lists.route('/move_entry/<int:moved_entry_id>/<int:list_id>', methods=['PUT'])
@login_required
def move_entry(moved_entry_id: int = None, list_id: int = None):
    #logger.debug(f'move_entry called moved_entry_id: {moved_entry_id}, list_id: {list_id}')
    #1. get the id of the entry being dragged
    if not moved_entry_id:
        moved_entry_id = int(request.form.get('moved_entry_id'))
    moved_entry = db.get_or_404(UserListEntry, moved_entry_id)
    is_list = request.form.get('is_list') == 'true'
    #logger.debug(f'is_list: {is_list}')
    #2. get the entry.id of the entry the moved_entry_id is being dropped on
    list_id = request.form.get('list_id')
    if list_id == 'undefined':
        list_id = None
    else:
        list_id = int(list_id)
    #logger.debug(f'list_id: {list_id}')
    if not list_id or not is_list:
        recieving_entry_id = int(request.form.get('recieving_entry_id'))  
        #3. if a userlist with parent_id == recieving_entry_id exists: change moved_entry.userlist_id to the userlist.id
        recieving_entry = db.get_or_404(UserListEntry, recieving_entry_id)
        recieving_item_model = recieving_entry.item_model
        #logger.debug(f'recieving_entry_id: {recieving_entry_id} name: {recieving_entry.get_item().name} recieving_item_model: {recieving_item_model}')     
        new_list = get_userlist(item_model=recieving_item_model, parent_entry_id=recieving_entry_id)
        #logger.debug(f'new_list after get_userlist: {new_list}')
        #else: create a new list with the dragged-over-task.name as the list name, dragged-over-task.id as parent
        if not new_list:
            #logger.debug(f'not new_list')
            new_list_name = f'{db.get_or_404(UserListEntry, recieving_entry_id).get_item().name} Sublist'
            #logger.debug(f'new_list_name: {new_list_name}')
            new_list = create_user_list(list_type=recieving_item_model, list_name=new_list_name, parent_entry_id=recieving_entry_id)
            #logger.debug(f'new_list after create_user_list: {new_list}')
        #4. add the dropped task to the list by changing the dragged-task.user_list_id to the list.id
        moved_entry.user_list_id = new_list.id
        #logger.debug(f'moved_entry.user_list_id: {moved_entry.user_list_id} = new_list.id: {new_list.id}')
    else:
        new_list = db.get_or_404(UserList, list_id)
        moved_entry.user_list_id = list_id
    order_index = request.form.get('order_index')
    if order_index:
        moved_entry.order = int(order_index)
    db.session.commit()
    flash(f'Entry {moved_entry_id} moved to list {new_list.list_name}')
    '''#logger.debug(f'moved_entry_id: {moved_entry_id} name: {moved_entry.get_item().name}, '
            f'new_list.parent_entry_id: {new_list.parent_entry_id},'
            f'new_list_id: {moved_entry.user_list_id}, new_list_name: {new_list.list_name}'
        )'''
    #5. return
    return ('', 204)

@lists.route('/update/<int:entry_id>', methods=['PUT'])
@login_required
def update(entry_id): #currently only for tasks
    entry = db.get_or_404(UserListEntry, entry_id)
    #logger.debug(f'entry_id: {entry_id}, entry.item_model: {entry.item_model}')
    if entry.item_model == 'Task':
        #logger.debug(f'test')
        task = entry.get_item()
        is_checked = request.form.get('isChecked')#, 'off') == 'on'
        #logger.debug(f'is_checked: {is_checked}')
        if is_checked:
            #logger.debug(f'{task.name} is_checked: {is_checked}')
            task.mark_as_completed()
        else:
            task.mark_as_pending()
    return ('', 204)

@lists.route('/update_list_order/', methods=['PUT', 'POST', 'DELETE', 'GET'])
@lists.route('/update_list_order/<int:list_id>', methods=['PUT', 'POST', 'DELETE', 'GET'])
@login_required
def update_list_order(list_id: int = None):
    hidden_list_id = request.form.get('hidden_list_id')
    if not list_id:
        raise ValueError('list_id cannot be None')
        if hidden_list_id is not None and hidden_list_id != '':
            list_id = int(hidden_list_id)
    order = request.form.getlist('items')
    #logger.debug(f'list_id: {list_id}, order1: {order}')
    if not order:
        userlist = db.get_or_404(UserList, list_id)
        order = db.session.scalars(select(UserListEntry).filter_by(user_list_id=userlist.id).order_by(UserListEntry.order)).all()
        #logger.debug(f'UserList {userlist.list_name} order2: {order}')
        if order is None or len(order) == 0:
            flash(f'No items in list {userlist.list_name}')
            #logger.debug(f'No items in list {userlist.list_name}')
            return ('', 204) #redirect(url_for('lists.show_list', list_id=list_id))
    # Extract the IDs if they are UserListEntry objects
    if hasattr(order[0], 'id'):
        #logger.debug(f'UserList {userlist.list_name} order3: {order}')
        order = [entry.id for entry in order]
    #logger.debug(f'order3: {order}')
    for index, entry_id in enumerate(order):
        #logger.debug(f'index: {index}, entry_id: {entry_id}')
        entry = update_entry_order(entry_id, index)
        #logger.debug(f'entry B: {entry}')
        #if not entry:
            #logger.debug(f'Entry {entry_id} not found')
            # Respond with an X-Revert header
            #response = make_response("")
            #revert = True
            #if revert:
            #    response.headers['X-Revert'] = 'true'
            #return response
            #return ('', 204)
        #else:
            #logger.debug(f'Updating entry_id: {entry_id} item_name: {entry.get_item().name} with new order: {index}')
    flash('List order updated')
    return ('', 204) #redirect(url_for('lists.show_list', list_id=list_id))

@lists.route('/show_list/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@lists.route('/show_list/<int:list_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def show_list(list_id: int = None):
    reversed = request.args.get('reversed') == 'True'
    #if reversed:
        #logger.debug(f'reverse true?: {reversed}')
    view_override = request.args.get('view_override')
    if view_override:
        view = view_override
    else:
        view = session.get('view')
    #logger.debug(f'view: {view}')
    #logger.debug(f'list_id1: {list_id}')
    sublevel_limit = request.args.get('sublevel_limit')
    #logger.debug(f'sublevel_limit: {sublevel_limit}')
    if sublevel_limit:
        sublevel_limit = int(sublevel_limit)
    else:
        sublevel_limit = 0
    sublevel = request.args.get('sublevel')
    if sublevel:
        sublevel = int(sublevel)
    else:
        sublevel = 0
    #logger.debug(f'sublevel: {sublevel}')
    #logger.debug(f'showing list list_id: {list_id}')
    force_new_list = request.args.get('force_new_list') == 'true'
    if list_id:
        list_obj=db.get_or_404(UserList, list_id)
        #logger.debug(f'list_obj with list_id {list_id}: {list_obj}')
        found_lists = [list_obj]
    elif not list_id:
        #logger.debug(f'not list_id')
        combine = bool(request.args.get('combine') == 'True')
        root_parent = request.args.get('root_parent')
        parent = request.args.get('parent')
        parent_entry_id = request.args.get('parent_entry_id')
        #logger.debug(f'force_new_list: {force_new_list}')  
        if parent_entry_id:
            parent_entry_id = int(parent_entry_id)
        elif parent:
            #logger.debug(f'parent1: {parent}')
            parent_entry_id = get_list_entries_for_item(parent)[0].id
            #logger.debug(f'parent_entry_id A: {parent_entry_id}')
        elif root_parent:
            root_parent_entry_id = get_list_entries_for_item(root_parent)[0].id
            #logger.debug(f'root_parent_entry_id: {root_parent_entry_id}')
        #logger.debug(f'parent_entry_id B: {parent_entry_id}')
        list_model = request.args.get('list_type')
        #logger.debug(f'list_model: {list_model}')
        if not list_model and parent_entry_id:
            found_lists = get_userlists_by_parent(parent_entry_id)
        elif root_parent:
            found_lists = get_top_userlists_by_root_parent(root_parent_entry_id, model=list_model)
        elif not list_model and not parent_entry_id:
            raise ValueError('No list type or parent entry id specified')
        else: #if list_model is not None
            if list_model == 'Home':
                if not parent_entry_id and not combine: 
                    parent_entry_id = None
            elif list_model == 'Floor':
                if not parent_entry_id and not combine: 
                    parent_entry_id = get_list_entries_for_item(current_user.active_home)[0].id
            elif list_model == 'Room':
                if not parent_entry_id and not combine: 
                    parent_entry_id = get_list_entries_for_item(current_user.active_home.active_floor)[0].id 
            elif list_model == 'Task':
                if not parent_entry_id and not combine: 
                    parent_entry_id = get_list_entries_for_item(current_user.active_home.active_room)[0].id   
                #logger.debug(f'show_list: Task list parent_entry_id C: {parent_entry_id}')
            elif list_model == 'Photo':
                if not parent_entry_id and not combine: 
                    parent_entry_id = get_list_entries_for_item(current_user.active_home.active_room)[0].id
            elif list_model == 'Pin':
                raise ValueError(f'Pin list should be served by the parent photo')
                '''if not parent_entry_id and not combine: 
                    parent_entry_id = get_list_entries_for_item(current_user.active_home.active_room.)[0].id'''
            else:
                raise ValueError(f'Unknown list type {list_model}')
            # if combine is True, show combined lists, else show the first list found
            list_obj = get_userlist(list_model, parent_entry_id=parent_entry_id, combine=combine)
            #logger.debug(f'list_obj A: {list_obj}')
            if not list_obj and force_new_list:
                list_obj = create_list_and_item_and_entry(list_model, retrieve='list')
            #logger.debug(f'list_obj B: {list_obj}')
            found_lists = [list_obj]
    if any(found_lists):
        child_lists = get_immediate_child_lists(found_lists)
        #logger.debug(f'found_lists - inner return: {found_lists}')
        return render_template('lists/list.html.jinja', userlists=found_lists, view=view, reversed=reversed, sublevel=sublevel, sublevel_limit=sublevel_limit, view_override=view_override, child_lists=child_lists)
    else:
        #logger.debug("no lists found - return")
        return '', 204
    #logger.debug(f'found_lists - outer return: {found_lists}')
    return render_template('lists/list.html.jinja', userlists=found_lists, view=view, reversed=reversed, sublevel=sublevel, sublevel_limit=sublevel_limit, view_override=view_override)

@lists.route('/show_photo_entry/<int:photo_id>', methods=['GET'])
@login_required
def show_photo_entry(photo_id):
    photo = db.get_or_404(Photo, photo_id)
    entry_id = get_list_entries_for_item(photo, list_type='Photo')[0].id
    photo_entry = db.get_or_404(UserListEntry, entry_id)
    return render_template('lists/model/photo.html.jinja', entry=photo_entry)


@lists.route('/rename/<string:item_model>/<int:item_id>', methods=['GET', 'PUT'])
@login_required
def rename_item(item_model, item_id):
    model_class = globals().get(item_model)
    if not model_class or not issubclass(model_class, db.Model):
        raise ValueError(f'Unknown item type {item_model}')
    
    item = db.get_or_404(model_class, item_id)
    
    entry = get_list_entries_for_item(item)[0]
    
    if request.method == 'GET':
        return render_template('lists/rename.html.jinja', entry=entry)
    if request.method == 'PUT':
        prev_name = request.form.get('placeholder')
        model_class = globals().get(item_model)
        if not model_class or not issubclass(model_class, db.Model):
            raise ValueError(f'Unknown item type {item_model}')
        item = db.get_or_404(model_class, item_id)
        #logger.debug(request.form)
        new_name = request.form.get(f'input_{item_model}_name-{item_id}')
        if not new_name or new_name == '':
            #logger.debug(f'prev_name: {prev_name}')
            return render_template('lists/name.html.jinja', entry=entry)
            #return prev_name, 200
        if item:
            #logger.debug(f'Found item: {item.name} to rename to: {new_name}')
            item.name = new_name
            #logger.debug(f'renaming item_model: {item_model}, item_id: {item_id} to {new_name}')
            db.session.commit()
            return render_template('lists/name.html.jinja', entry=entry)

@lists.route('/delete/entry/<int:user_list_entry_id>', methods=['DELETE'])
@login_required
def delete(user_list_entry_id):
    code = request.args.get('code')
    if not code: # if swap is not set to 'delete'
        code = 204
    #logger.debug(f'code: {code}')
    if delete_entry_and_item(user_list_entry_id):
        flash(f'user_list_entry_id: {user_list_entry_id} Item deleted', 'danger')
        #logger.debug(f'deleted user_list_entry_id: {user_list_entry_id} Item deleted')
    else:
        flash('Item not found', 'danger')
        #logger.debug('Item to delete not found')
    return ('', code)

@lists.route('/delete/list/<int:user_list_id>', methods=['DELETE'])
@login_required
def delete_list(user_list_id):
    code = request.args.get('code')
    if not code:
        code = 204
    raise NotImplementedError('delete userlist not yet implemented')
    if delete_entry_and_item(user_list_entry_id):
        flash(f'user_list_entry_id: {user_list_entry_id} Item deleted', 'danger')
    else:
        flash('Item not found', 'danger')
    return ('', 204)
# [ ] Cleanup unused routes when finished and testing complete