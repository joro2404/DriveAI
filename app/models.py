from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Boolean, ForeignKey('role.id'), nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    phone_number = db.Column(db.Text, nullable=True)

    def __init__(self, id, username, first_name, last_name, email, password, phone_number):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Emotions(db.Model):
    __tablename__ = "emotions"

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Statistics(db.Model):
    __tablename__ = "statistics"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Boolean, ForeignKey('users.id'), nullable=False)
    emotion_id = db.Column(db.Boolean, ForeignKey('emotions.id'), nullable=False)
    time = db.Column(db.TIMESTAMP, primary_key=True)
    pasengers_count = db.Column(db.Integer, nullable=False)

    def __init__(self, id, driver_id, time, emotion_id):
        self.id = id
        self.driver_id = driver_id
        self.time = time
        self.emiotionaly = emotion_id