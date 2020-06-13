
from flask_sqlalchemy import SQLAlchemy


from . import db


class Measurement(db.Model):
    __tablename__ = "measurements"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    location = db.Column(db.String)
    # created_by = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return f"<Measurement {self.value}>"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    measurements = db.relationship('Measurement', backref='user')

    def __repr__(self):
        return f"<Name {self.display_name}>"


class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Name {self.location}>"
