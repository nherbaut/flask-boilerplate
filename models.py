from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from app import db
from sqlalchemy.orm import relationship
engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.


class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    rdvs = relationship("RDV", cascade="all")

    def __init__(self, name=None, password=None,email=None):
        self.name = name
        self.password = password
        self.email=email


class RDV(Base):
    __tablename__ = 'RDV'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), )
    time  = db.Column(db.String(120), )
    nature = db.Column(db.String(120), )
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")


    def __init__(self, title=None,time=None,nature=None,user_id=None):
        self.title = title
        self.time  = time
        self.nature = nature
        self.user_id = user_id
        
    

    




# Create tables.
Base.metadata.create_all(bind=engine)
