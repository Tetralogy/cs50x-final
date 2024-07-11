from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cleaning_tracker.db"
# initialize the app with the extension
db.init_app(app)


# Define models
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='room', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

# Routes
@app.route('/')
def home():
    rooms = Room.query.all()
    return render_template('home.html', rooms=rooms)

@app.route('/add_room', methods=['POST'])
def add_room():
    room_name = request.form['room_name']
    new_room = Room(name=room_name)
    db.session.add(new_room)
    
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/room/<int:room_id>')
def room(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room.html', room=room)

@app.route('/add_task/<int:room_id>', methods=['POST'])
def add_task(room_id):
    task_description = request.form['task_description']
    new_task = Task(description=task_description, room_id=room_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('room', room_id=room_id))

@app.route('/toggle_task/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('room', room_id=task.room_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)