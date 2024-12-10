from typing import List, Optional
from flask import flash
from flask_login import current_user
from sqlalchemy import and_, select
from application.database.models import Floor, Home, Photo, Room, RoomDefault, Task, UserList, UserListEntry
from application.extension import db


def create_user_list(list_type: str, list_name: str, parent_entry_id: int = None) -> UserList:
    if not list_type:
        raise ValueError('list_type argument is required')
    if not list_name:
        list_name = default_list_name(list_type, parent_entry_id)
    # Split the list_type if it contains ' ComboList'
    if 'ComboList' in list_type:
        base_list_type = list_type.replace(' ComboList', '')
        model_class = globals().get(base_list_type)
    else:
        model_class = globals().get(list_type)
    if not model_class or not issubclass(model_class, db.Model) and 'ComboList' not in list_type:
        raise ValueError(f'Unknown list type {list_type}')
    existing_list = db.session.execute(
        select(UserList).filter_by(user_id=current_user.id, list_name=list_name)
    ).scalar()
    if existing_list:
        return existing_list
    new_list = UserList(user_id=current_user.id, list_name=list_name, list_type=list_type, parent_entry_id=parent_entry_id)
    print(f'create_user_list: new_list: {new_list}')
    db.session.add(new_list)
    db.session.commit()
    return new_list
def default_list_name(item_model, parent_entry_id: int=None, room_id: int=None):
    if not item_model:
        raise ValueError('item_model cannot be None')
    print(f'default_list_name() A: item_model: {item_model}, parent_entry_id: {parent_entry_id}')
    if not parent_entry_id:
        if not room_id:
            room_id = current_user.active_home.active_room_id
            if not room_id:
                raise ValueError('No active room or parent_entry_id provided')
        print(f'room_id: {room_id}')
        room = db.get_or_404(Room, room_id)
        parent = room
        parent_entry_id = get_list_entries_for_item(room)[0].id
        item_name = room.name
    else:
        parent = db.get_or_404(UserListEntry, parent_entry_id)
        item_name = parent.get_item().name
    list_name = f'{item_name} {item_model}s'
    print(f'default_list_name() B: list_name: {list_name} parent_entry_id: {parent_entry_id}')
    return list_name, parent_entry_id
def add_item_to_list(user_list_id: int, item_model: str, item_id: int = None, order: int = None, name: str = None, photo_url: str = None) -> UserListEntry:
    list_obj = db.get_or_404(UserList, user_list_id)
    print(f'add_item_to_list(): user_list_id: {user_list_id}, item_model: {item_model}, item_id: {item_id}, order: {order}, name: {name}')
    if not list_obj:
        raise ValueError(f'Unknown list id {user_list_id}')
    if item_model is None:
        raise ValueError('item_model cannot be None')
    model_class = globals().get(item_model)
    if not model_class or not issubclass(model_class, db.Model):
        raise ValueError(f'Unknown item type {item_model}')
    if item_id is None:
        new_item = create_new_default(item_model, name, list_obj, photo_url=photo_url)
        if not new_item:
            return None
        item_id = new_item.item_id
    if order is None:
        order = db.session.scalars(db.select(db.func.count()).select_from(UserListEntry).where(UserListEntry.user_list_id == user_list_id)).one()
    elif order < 1:
        all_items = db.session.scalars(db.select(UserListEntry).filter_by(user_list_id=user_list_id).order_by(UserListEntry.order)).all()
        for item in all_items:            
            item.order += 1
        db.session.commit()
        order = 0
    else:
        all_items = db.session.scalars(db.select(UserListEntry).filter_by(user_list_id=user_list_id).order_by(UserListEntry.order)).all()
        if any(item.order == order for item in all_items):
            order += 1
        for item in all_items:
            if item.order >= order:
                item.order += 1
    new_list_item = UserListEntry(user_list_id=user_list_id, item_model=item_model, item_id=item_id, order=order)
    db.session.add(new_list_item)
    db.session.commit()
    return new_list_item

def create_new_default(item_model: str, name: str = None, list_obj: UserList = None, photo_url: str = None) -> UserListEntry:
    print(f'create_new_default(): item_model: {item_model}, name: {name}')
    if item_model == 'Home':
        if not name:
            user_home_count = db.session.query(Home).filter_by(user_id=current_user.id).count()
            name = f'{current_user.username} Home {user_home_count + 1}'
        new_item = Home(user_id=current_user.id, name=name)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Floor':
        print(f'name (create_new_default):  {name}')
        current_home = current_user.active_home
        if not name:
            floor_name = set_default_floor_name()
        else:
            floor_count = current_user.active_home.floors.count()
            if floor_count == 0:
                floor_name = set_default_floor_name()
            else:
                count = 0
                existing_floors = db.session.scalars(db.select(Floor.name).filter(Floor.home_id == current_home.id)).all()
                for floor_name in existing_floors:
                    if name in floor_name:
                        count += 1
                    floor_name = f'{name} {count + 1}'
                    print(f'floor_name (create_new_default): {floor_name}')
        new_item = Floor(home_id=current_home.id, name=floor_name) #creates default floor
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Task':
        if not name:
            room_task_count = int(len(list_obj.entries))
            print(f'room_task_count: {room_task_count}')
            name = f"{current_user.active_home.active_room.name} {item_model} {room_task_count + 1}"
            print(f'name (create_new_default): {name}')
        new_item = Task(user_id=current_user.id, name=name)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Room':
        if not name:
            name = item_model
        room_type = name
        same_type_rooms_count = db.session.execute(
            select(db.func.count())
            .select_from(Room)
            .where(and_(Room.home_id == current_user.active_home_id, Room.room_type == room_type))
        ).scalar() 
        print(f'same_type_rooms_count: {same_type_rooms_count}')
        
        newname = f'{room_type} {same_type_rooms_count + 1}'
        print(f'room (create_new_default): {newname}')
        new_item = Room(home_id=current_user.active_home_id, floor_id=current_user.active_home.active_floor_id, room_type=room_type, name=newname)
        db.session.add(new_item) 
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'RoomDefault':
        if not name:
            raise ValueError('name for RoomDefault cannot be None')
        existing_item = db.session.scalars(db.select(RoomDefault.name).filter_by(name=name, user_id=current_user.id)).first()
        if existing_item:
            flash(f'RoomDefault: "{name}" already exists', 'error')
            return None 
            raise ValueError(f'A RoomDefault with the name "{name}" already exists.')
        new_item = RoomDefault(user_id=current_user.id, name=name)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    if item_model == 'Photo':
        if not name:
            raise ValueError('name for Photo cannot be None')
            room_photo_count = int(len(list_obj.entries))
            print(f'room_photo_count: {room_photo_count}')
            name = f"{filename} {current_user.active_home.active_room.name} {item_model} {room_photo_count + 1}"
            print(f'name (create_new_default): {name}')

        description = name 
        print(f'photo_url: {photo_url}')
        print(f'description: {description}')
        
        # Create a new Photo item for each uploaded file
        new_item = Photo(
            user_id=current_user.id, 
            room_id=current_user.active_home.active_room_id, 
            name=name,
            description=description, 
            photo_url=photo_url
        )
        db.session.add(new_item)
            
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    #todo: photopin 
    if item_model == 'Pin':
        #xxx new_item = Pin(task_id= #BUG GET TASK ID for pin, photo_id= #BUG GET PHOTO ID for pin)
        db.session.add(new_item)
        db.session.commit()
        return UserListEntry(item_model=item_model, item_id=new_item.id)
    else:
        raise ValueError(f'Unknown item type {item_model}')
''' uploaded_files 
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
def get_userlists_by_parent(parent_entry_id: int) -> List[UserList]:
        lists = current_user.lists.filter_by(parent_entry_id=parent_entry_id).all()
        if lists:
            print(f'get_userlists_by_parent: lists found (parent_entry_id){parent_entry_id}: {lists}')
        else:
            print(f'get_userlists_by_parent: No lists found for parent_entry_id {parent_entry_id}')
        return lists

def get_top_userlists_by_root_parent(root_parent_entry_id: int, model) -> List[UserList]:
        if not model:
            raise ValueError('model cannot be None')
        print(f'input root_parent_entry_id: {root_parent_entry_id} model: {model}')
        parent_entry_id=root_parent_entry_id
        parent_lists = get_userlists_by_parent(parent_entry_id=root_parent_entry_id) # -> List[UserList]:
        parent_lists_with_model = [userlist for userlist in parent_lists if userlist.list_type == model]
        while not parent_lists_with_model and parent_lists:
            found_lists = []
            for userlist in parent_lists:
                for entry in userlist.entries:
                    child_lists = get_userlists_by_parent(parent_entry_id=entry.id)
                    found_lists.extend(child_lists)
            parent_lists_with_model = [userlist for userlist in found_lists if userlist.list_type == model]
            parent_lists = found_lists
        if parent_lists_with_model:
            print(f'get_top_userlists_by_root_parent: lists found (parent_entry_id){root_parent_entry_id}: {parent_lists_with_model}')
        else:
            print(f'get_top_userlists_by_root_parent: No {model} lists found for root_parent_entry_id {root_parent_entry_id}')
        return parent_lists_with_model

def get_immediate_child_lists(parent_lists: List[UserList]) -> List[UserList]:
    found_lists = {}
    for parent_list in parent_lists:
        for entry in parent_list.entries:
            child_lists = get_userlists_by_parent(parent_entry_id=entry.id)
            if parent_list not in found_lists:
                found_lists[parent_list] = []
            found_lists[parent_list].extend(child_lists)
    return found_lists

def get_userlist(item_model: str = None, list_name: str = None, parent_entry_id: int = None, combine: bool = False): #gets the primary list of a main model
    print(f'get_userlist(): item_model: {item_model}, list_name: {list_name}, parent_entry_id: {parent_entry_id}')
    if not item_model and not parent_entry_id:
        raise ValueError("Must provide item_model or parent_entry_id argument")
    if all((item_model, list_name, parent_entry_id)):
        lists = current_user.lists.filter_by(list_type=item_model, list_name=list_name, parent_entry_id=parent_entry_id).all()
        combolist_name = f'Combo {item_model} {list_name} {parent_entry_id}'
        print(f'lists found (All args): {lists}')
    elif item_model and not list_name and not parent_entry_id:
        lists = current_user.lists.filter_by(list_type=item_model).all()
        combolist_name = f'Combo All {item_model}'
        print(f'lists found (model): {lists}')
    elif item_model and not list_name and parent_entry_id:
        lists = current_user.lists.filter_by(list_type=item_model, parent_entry_id=parent_entry_id).all()
        combolist_name = f'Combo {item_model} {parent_entry_id}'
        print(f'lists found (model, parent): {lists}')
    elif item_model and list_name and not parent_entry_id:
        lists = current_user.lists.filter_by(list_type=item_model, list_name=list_name).all()
        combolist_name = f'Combo {item_model} {list_name}'
        print(f'lists found (model, name): {lists}')
    else:
        lists = current_user.lists.filter_by(parent_entry_id=parent_entry_id).all()
        combolist_name = f'Combo {parent_entry_id}'
        print(f'lists found (parent_entry_id): {lists}')
    
    if not lists:
        print(f'No lists of type {item_model} found for user {current_user.id}')
        return None
    if len(lists) == 0:
        print(f'len(lists) == 0: {list_name} {item_model} {parent_entry_id}')
        return None
        raise ValueError(f'No lists of type {item_model} found for user {current_user.id}')
    if len(lists) > 1:
        print(f'len(lists) > 1: {lists}')
        print(f'combine: {combine}')
        # combine the lists into a single UserList object
        if combine:
            userlist = combine_userlists(userlists = lists, combolist_name=combolist_name, parent_entry_id=parent_entry_id)
        else:
            userlist = lists[0]
        
        return userlist
    else:
        print(f'len(lists) == 1: {list_name} {item_model} {parent_entry_id}')
        list_id = lists[0].id
    if not isinstance(list_id, int):
        raise ValueError(f'No lists of type {item_model} found for user {current_user.id}')
        if isinstance(list_id, str):
            item_model = list_id
            lists = current_user.lists.filter_by(list_type=item_model).all()
            if len(lists) == 0:
                raise ValueError(f'No lists of type {item_model} found for user {current_user.id}')
            if len(lists) > 1:
                print('More than one list matches the string. Please select one:')
                for i, lst in enumerate(lists):
                    print(f'{i+1}. {lst.list_name}')
                selected_list_index = int(input('Enter the number of the list: '))
                list_id = lists[selected_list_index-1].id
            else:
                list_id = lists[0].id
    userlist =  db.get_or_404(UserList, list_id)
    newlist = []
    print(f'userlist.entries: {userlist.entries} List type: {type(userlist.entries)}')
    for entry in userlist.entries:
        print(f'List: {entry.user_list.list_name}, Order: {entry.order}')
        #newlist.append(entry.get_item().as_list_item)
    return userlist

def combine_userlists(userlists: List[UserList], combolist_name: str = None, parent_entry_id: int = None) -> UserList:
    # search all userlists in the list and see if they have the same list_type
    if all(userlist.list_type == userlists[0].list_type for userlist in userlists):
        print("All userlists have the same list_type")
        list_type = userlists[0].list_type
    else:
        print("Not all userlists have the same list_type")
        list_type = 'Mixed'
    list_type = f'{list_type} ComboList'
    if not combolist_name:
        combolist_name = list_type
    print(f'list_name: {combolist_name}')
    if not parent_entry_id:
        if all(userlist.parent_entry_id == userlists[0].parent_entry_id for userlist in userlists):
            parent_entry_id = userlists[0].parent_entry_id
        else:
            parent_entry_id = get_list_entries_for_item(current_user.active_home)[0].id
    combined_list = get_userlist(list_type, combolist_name, parent_entry_id=parent_entry_id)
    if not combined_list:
        print(f'combined_list not found, creating new list')
        combined_list = create_user_list(list_type, combolist_name, parent_entry_id=parent_entry_id)
    print(f'combined_list?: {combined_list}')
    for userlist in userlists:
        for entry in userlist.entries:
            print(f'entry: {entry}')
            # check if item_id is already in combined_list
            if entry.item_id not in [item.item_id for item in combined_list.entries]:
                #extract item_id from each entry
                #add each item_id as a new entry to the new UserList combined list
                new_list_item = add_item_to_list(user_list_id=combined_list.id, item_model=entry.item_model, item_id=entry.item_id, order=entry.order)
                print(f'new_list_item: {new_list_item}')
    return combined_list

def get_list_entries_for_item(item: object, list_type: str = None, user_id: int = None) -> List[UserListEntry]:
    if not item:
        raise ValueError('item cannot be None')
    if isinstance(item, str):
        input_string = item
        words = input_string.strip("<>").split()
        item_model = words[0]
        item_id = int(words[1])
        print(f'input_string: {input_string}, item_model: {item_model}, item_id: {item_id}')
        model_class = globals().get(item_model)
        item = db.get_or_404(model_class, item_id) # Convert string to the original object
    if not user_id:
        user_id = current_user.id
    if not list_type:
        list_type = item.__class__.__name__
    # Find all list entries associated with this task
    found_entries = UserListEntry.find_entries_for_item(item)
    if not found_entries:
        raise ValueError(f'No list entries found for item: {item}')
    print(f'found_entries for {item}: {found_entries}')
    # Now you can iterate through the list entries
    list_entries = []
    if user_id: # must belong to specified user, default to current_user
        for entry in found_entries:
            if not entry.user_list or not entry.user_list.user_id:
                print(f'Entry without user: {entry}')
            elif entry.user_list.user_id == user_id and entry.user_list.list_type == list_type:
                print(f'Entry: {entry}')
                print(f"Item Model: {entry.item_model}, Item ID: {entry.item_id}")
                print(f'User List ID: {entry.user_list.id} User List Name: {entry.user_list.list_name}')
                print(f'user: {entry.user_list.user_id}')
                list_entries.append(entry)
            else:
                print(f'Entry does not belong to current_user: {entry}')
    else: # belongs to any user if user_id is None
        list_entries = found_entries
    return list_entries

def get_child_user_lists(entry_id: int) -> List[UserList]:
    # Fetch the UserListEntry
    entry = db.session.scalars(db.select(UserListEntry).filter_by(id=entry_id)).one_or_none()
    if not entry:
        raise ValueError(f'No UserListEntry found with id: {entry_id}')
    
    # Find all UserLists where parent_entry_id matches the given entry_id
    child_user_lists = db.session.scalars(
        db.select(UserList)
        .filter_by(parent_entry_id=entry_id)
        .distinct()  # Ensure the results are unique
    ).unique().all()
    
    return child_user_lists

# up tree: starting from a child entry; use (user_list_id to get list > parent_entry_id) until 'specified high level entry_id'
# down tree: starting from the specified parent_entry_id; use (find lists containing parent_entry_id to get child_user_lists > for list in child_user_lists > user_list > for entry in user_list.entries > entry) until 'specified low level entry_id'

def build_hierarchy(parent_entry_id: int) -> dict: #[ ]: remove if unnecessary
    from collections import deque
    hierarchy = {}
    queue = deque([parent_entry_id])
    print(f'queue: {queue}')
    level_counter = 0
    while queue:
        current_entry_id = queue.popleft()
        
        # Get the child user lists for the current entry
        child_user_lists = get_child_user_lists(current_entry_id)
        
        for user_list in child_user_lists:
            hierarchy[user_list.id] = {
                'list': user_list,
                'list_name': user_list.list_name,
                'parent_entry_id': user_list.parent_entry_id,
                'entries': []
            }
            
            for entry in user_list.entries:
                # Add the entry's ID to the queue to process its children
                queue.append(entry.id)
                
                # Add the entry to the list's children
                hierarchy[user_list.id]['entries'].append(entry.id)
        level_counter += 1
        #print(f'level_counter: {level_counter}')
    print(f'level_counter at end: {level_counter}')
    return hierarchy

def print_hierarchy_iterative(hierarchy: dict, parent_entry_id: int = None): # [ ]: remove if unnecessary
    print("print_hierarchy_iterative:")
    stack = [(parent_entry_id, 0)]  # Stack to track (current_parent_id, current_indent)

    while stack:
        current_parent_id, indent = stack.pop()

        for user_list_id, user_list_data in hierarchy.items():
            if user_list_data['list'].parent_entry_id == current_parent_id:
                print('  ' * indent + f"UserList {user_list_id}:")
                print('  ' * indent + f"  Entries: {user_list_data['entries']}")
                print()
                # Add child lists to the stack with increased indentation
                stack.append((user_list_id, indent + 1))
def unpack_hierarchy(hierarchy: dict) -> List[dict]:
    raise NotImplementedError("unpack_hierarchy not yet implemented") # [ ]: remove if unnecessary
def update_entry_order(user_list_entry_id: int, new_order: int) -> Optional[UserListEntry]:
    print(f'user_list_entry_id: {user_list_entry_id}, new_order: {new_order}')
    entry = db.session.scalars(db.select(UserListEntry).filter_by(id=user_list_entry_id)).one_or_none()
    #entry = UserListEntry.query.get(user_list_entry_id)
    print(f'entry A: {entry}')
    if new_order is None:
        return None
    if entry:
        entry.order = new_order
        db.session.commit()
        return entry
    return None

def delete_entry_and_item(user_list_entry_id: int) -> bool:
    userlist_entry = UserListEntry.query.get(user_list_entry_id)
    
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

'''def add_custom_item_to_list(user_list_id: int, name: str, order: int, custom_data: str = None) -> UserListEntry:
    new_item = UserListEntry(user_list_id=user_list_id, item_type='custom', item_id=0, order=order, custom_data=custom_data)
    db.session.add(new_item)
    db.session.commit()
    return new_item'''

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