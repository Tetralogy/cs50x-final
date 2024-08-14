'''def create_home():
    


def create_room():
    


def create_task


def create_recommendation


def create_note


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup
Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)

# Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)

# CRUD Operations
def crud_operations():
    session = Session()

    # Create
    def create():
        field = input(f"{field}: ")
        
    new_user = User(name="Alice", age=30)
    session.add(new_user)
    session.commit()

    # Read
    user = session.query(User).filter_by(name="Alice").first()
    print(f"Read: {user.name}, {user.age}")

    # Update
    user.age = 31
    session.commit()

    # Delete
    session.delete(user)
    session.commit()

    session.close()

crud_operations()'''