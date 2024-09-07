from functools import wraps
import time
from flask import Blueprint, flash, g, get_flashed_messages, redirect, render_template, request, session

utils = Blueprint('utils', __name__)

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    flash(f'{message}, {code}')
    return render_template("apology.html", top=code, bottom=escape(message)), code


def handle_error(error):
    error_code = getattr(error, 'code', 500)  # default to 500 if code attribute doesn't exist
    return apology(f"An error occurred: {str(error)}", code=error_code)

    
@utils.route('/get-flash-messages')
def get_flash_messages():
    messages = get_flashed_messages(with_categories=True)
    print(f"Retrieved flash messages: {messages}")
    return render_template('base/parts/flash_messages.html.jinja' , messages=messages)

@utils.route('/remove-flash')
def remove_flash():
    return '', 200  # Return empty response


def detect_recursive_rendering(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        template = args[0]
        current_route = request.path
        
        if 'template_stack' not in session:
            session['template_stack'] = []
        if 'route_stack' not in session:
            session['route_stack'] = []
        if 'last_request_time' not in session:
            session['last_request_time'] = time.time()
        
        current_time = time.time()
        if current_time - session['last_request_time'] > 5:
            session['template_stack'] = []
            session['route_stack'] = []
        session['last_request_time'] = current_time
        
        if template in session['template_stack']:
            session['template_stack'] = []
            session['route_stack'] = []
            raise Exception(f"Recursive template loading detected: {template}")
        
        if current_route in session['route_stack']:
            session['template_stack'] = []
            session['route_stack'] = []
            raise Exception(f"Recursive route loading detected: {current_route}")
        
        session['template_stack'].append(template)
        session['route_stack'].append(current_route)
        session.modified = True
        
        try:
            return f(*args, **kwargs)
        finally:
            if session['template_stack']:
                session['template_stack'].pop()
            if session['route_stack']:
                session['route_stack'].pop()
            session.modified = True
    
    return decorated_function

def detect_recursive_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_route = request.path
        
        if 'route_stack' not in session:
            session['route_stack'] = []
        
        if current_route in session['route_stack']:
            session['route_stack'] = []
            raise Exception(f"Recursive route loading detected: {current_route}")
        
        session['route_stack'].append(current_route)
        session.modified = True
        
        try:
            return f(*args, **kwargs)
        finally:
            if session['route_stack']:
                session['route_stack'].pop()
            session.modified = True
    
    return decorated_function

# Automatically apply the decorator to all routes
def apply_recursive_detection(app):
    for endpoint, view_func in app.view_functions.items():
        app.view_functions[endpoint] = detect_recursive_route(view_func)
