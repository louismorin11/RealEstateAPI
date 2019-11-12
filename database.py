from flask_sqlalchemy import SQLAlchemy, event
from flask_login import UserMixin
from flask_marshmallow import Marshmallow
from config import db, ma


"""
@login_manager.user_loader
def get_user(ident):
    return User.query.filter_by(id=ident).first()
"""

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.Text)
    name = db.Column(db.Text)
    bday = db.Column(db.DateTime)    
    estate = db.relationship('Estate', backref="owner_estate", cascade="delete", lazy='dynamic')

class UserSchema(ma.ModelSchema):
    class Meta:
        id = fields.Int(dump_only=True)
        surname = fields.Str()
        name = fields.Str()
        bday = fiels.DateTime()
        estate = fields.Nested(EstateSchema, many=True, only=["name"])



class Estate(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    id_owner=db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    re_type = db.Column(db.Text)
    city = db.Column(db.Text)
    rooms = db.relationship('Room', backref="rl_room", cascade="delete", lazy='dynamic')

class EstateSchema(ma.TableSchema):
    class Meta:
        id = fields.Int(dump_only=True)
        description = fields.Str()
        name = fields.Str()
        re_type = fields.Str()
        bday = fiels.DateTime()
        city = fields.Str()
        rooms = fields.Nested(RoomSchema, many=True)
        id_owner = fields.Int()

class Room(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    id_estate=db.Column(db.Integer, db.ForeignKey("estate.id"))

class RoomSchema(ma.TableSchema):
    class Meta:
        id = fields.Int(dump_only=True)
        description = fields.Str()
