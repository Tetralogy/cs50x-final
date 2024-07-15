from flask import Flask
from database.models import db, User  # Assuming models.py is in a 'database' folder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db.init_app(app)

@app.route('/')
def index():
    return 'Hello, World! 111324654346535'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    #todo #3 test again