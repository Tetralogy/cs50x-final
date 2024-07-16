from flask import Flask
from database.models import db, User  # Assuming models.py is in a 'database' folder

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

db.init_app(app)

@app.route('/')
def index():
    return 'Hello, World! 111324654346535'
'''
app.route('/register', methods=['GET', 'POST'])
def register():
    return render template 'Register.html'


        #TODO: #5 Register/create an account
        #TODO: #6 Login
        #TODO: #7 Logout

        #TODO: #9 complete Onboarding experience loop
            #TODO: #8 initial questions and info input from user
            
            House size
        Number of levels
        Layout
        Important rooms
        Bedrooms
        Bathrooms
        kitchen
        Others
        Etc.
        
            #TODO: #10 User inputs self-assessment of abilities and disabilities
            #TODO: #11 Initial full home Walkthrough
            Systematically go to every room in the house to note workload
        App guides and prompts and User takes wide photo of each area to annotate later
        Interior spaces documented
        Exterior spaces if applicable based on user’s initial setup
        
        # TODO: #12 Annotation and organization of tasks
            #TODO: #13 User clicks on each area in the photos to be cleaned and maintained and is visually marked up
            Information about specific spots is entered
                Appliances
                Surface types per room
                General usage and lifestyle of spaces
                Frequency of use
                Importance
                Aesthetical issues
                Dirtiness and effort required
                Tools/supplies on hand
                Tools/supplies required
                
        #TODO: #14 Map of house with visualizations of amount of work and type of tasks is populated
            Markers, colors, graphs and other ways to show progress at a glance

#TODO: #15 A master task list is generated

#TODO: #16 create customtips and tricks and suggestions schema
'''
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    #todo #3 test again