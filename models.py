from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
import datetime

database_path = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCEHMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


cast_list = db.Table('cast_list',
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actor.id'), primary_key=True)
)

class Movie(db.Model):
    #__tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    actors = db.relationship('Actor', secondary=cast_list, backref=db.backref('movies', lazy=True))


class Actor(db.Model):
    #__tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)