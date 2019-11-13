#!/usr/bin/env python


from flask import request, jsonify, abort
from sqlalchemy.sql import func
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, Schema,INCLUDE
from database import  UserSchema, EstateSchema, RoomSchema


import config

from config import db, app


app = config.app
db.create_all()
"""
Check if the provided token is correct, returns the id of the user or -1 otherwise
"""
def check_user(req):
	from database import User
	if req and req.get('token'):	
		current_user = User.query.filter_by(token = req.get('token')).first() 	
		if current_user:
			return current_user.id
	return -1


@app.route('/')
def index():
    return "This is a RESTful API, please use the appropriate endpoints"

"""
Search enpoint, the name of the city is transmitted in a GET request

Returns all estate located in the given city, as JSON
"""
@app.route('/search/<city>', methods = ['GET'])
def search(city):	
	from database import Estate
	estates_schemas=EstateSchema(many=True)
	estates = Estate.query.filter_by(city=city.upper()).all()
	return jsonify(estates_schemas.dump(estates))

"""
Get all users, mainly for debug purposes
"""
@app.route('/users', methods = ['GET'])
def users():
	from database import User
	usersSchema = UserSchema(many = True)
	all_users = User.query.all()
	return jsonify(usersSchema.dump(all_users))


"""
Get a specific estate by id

Returns a JSON containing all information on the id
"""
@app.route('/estate/<id>', methods = ['GET'])
def get_estate(id):
	from database import Estate
	estate_schema = EstateSchema()
	estate = Estate.query.filter_by(id=id).first()
	if estate:
		return estate_schema.dump(estate)
	else:
		abort(400)


"""
Add estate enpoint, the parameters are transmitted in a POST request
I assume here that a user must be registered - i.e. have a token - to add an estate
Expected format is

Returns estate id
"""
@app.route('/add_estate', methods = ['POST'])
def add_estate():
	from database import Estate
	req = request.get_json(force=True) 
	owner = check_user(req)
	#we need to have a valid token
	if owner == -1:
		abort(401,"You must have a valid token to add an esate, use /register")
	#unkown = INCLUE guarantee that we will ignore the token field in the deserialization
	schem = EstateSchema(unknown=INCLUDE) 
	#test if the input json is well formated
	if schem.validate(req):
		return jsonify(schem.validate(req))
	else:		
		new_estate = schem.load(req)
		#set the owner as the user who sent the POST request
		new_estate.id_owner = owner
		#will generate room objects too
		db.session.add(new_estate)
		db.session.commit()
		return jsonify({'estate_id' : new_estate.id})
"""
Update estate enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
WARNING : the rooms field will be discarded, please use update_room, add_room or delete_room to update the rooms
Expected format is


Returns the new representation of the estate as JSON ?
"""
@app.route('/update_estate/<id>', methods = ['PUT'])
def update_estate(id):
	from database import Estate
	req = request.get_json(force=True) 
	owner = check_user(req) 
	estate = Estate.query.filter_by(id=id).first()
	if estate:
		if owner != estate.id_owner:
			abort(401,"You must be the owner of the estate to modifiy it, use the right token")
		schem = EstateSchema(unknown=INCLUDE)
		#test if the input json is well formated
		if schem.validate(request.get_json(force=True), partial=True):
			return jsonify(schem.validate(request.get_json(force=True),partial=True))
		else:		
			new_estate = schem.load(request.get_json(force=True), partial = True)			
			dico = (EstateSchema().dump(new_estate))
			#we discard all fields that are not specified and the rooms field
			dico = {key: val for key, val in dico.items() if (val is not None and (key !="rooms"))}
			#update all specified fields
			for key, val in dico.items():
				setattr(estate, key,val)
			db.session.commit()
			return jsonify({'estate_id' : estate.id})
	else:
		abort(400)

"""Add a room to estate id with given name and description 
If estate_id does not match with an actual estate, will not add a room

returns the id of the room created
"""
@app.route('/add_room', methods = ['POST'])
def add_room():
	from database import Room, Estate
	owner = check_user(request.get_json(force=True)) 
	schem = RoomSchema(unknown=INCLUDE)
	#test if the input json is well formated
	if schem.validate(request.get_json(force=True)):
		return jsonify(schem.validate(request.get_json(force=True)))
	else:		
		new_room = schem.load(request.get_json(force=True))
		est_id = new_room.id_estate
		if est_id and len(Estate.query.filter_by(id = est_id).all()) == 1:				
			source_estate = Estate.query.filter_by(id = est_id).first()
			if owner != source_estate.id_owner:
				abort(401,"You must be the owner of the estate to modifiy it, use the right token")
			#will generate room objects too
			db.session.add(new_room)
			db.session.commit()
			return jsonify({'new_room' : new_room.id})
		else:
			return jsonify({'error' : 'The given estate id does not match a correct estate'})


"""
Update user enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
Expected format is


Returns the id of the user that was modified
"""
@app.route('/update_room/<id>', methods = ['PUT'])
def update_room(id):
	from database import Room, Estate
	owner = check_user(request.get_json(force=True)) 
	room = Room.query.filter_by(id=id).first()
	source_estate = Estate.query.filter_by(id = room.id_estate).first()
	if owner != source_estate.id_owner:
			abort(401,"You must be the owner of the estate to modifiy it, use the right token")
	if room:
		schem = RoomSchema(unknown=INCLUDE)
		#test if the input json is well formated
		if schem.validate(request.get_json(force=True), partial=True):
			return jsonify(schem.validate(request.get_json(force=True),partial=True))
		else:		
			new_room = schem.load(request.get_json(force=True), partial = True)			
			dico = (RoomSchema().dump(new_room))
			#we discard all fields that are not specified
			dico = {key: val for key, val in dico.items() if (val is not None)}
			#update all specified fields
			for key, val in dico.items():
				setattr(room, key,val)
			db.session.commit()
			return jsonify({'room_id' : room.id})
	else:
		abort(400)



"""
User registration enpoint, the parameters are transmitted in a POST request
Expected format is


Returns a token associated to the user - for simplicity sake, these token do not expire 
This cannot be safe in a prod environnement, as the token is stored in plain text, but it will be used for symplicty
For a more traditionnal backend, I would use flask-login and sessions to restrict the access to certains users for a given set of endpoints
But this would not be stateless anymore
"""
@app.route('/register', methods = ['POST'])
def register():
	schem = UserSchema()
	#test if the input json is well formated
	if schem.validate(request.get_json(force=True)):
		return jsonify(schem.validate(request.get_json(force=True)))
	else:		
		new_user = schem.load(request.get_json(force=True))

		#will generate room objects too
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'token' : new_user.token})


"""
Update user enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
Expected format is


Returns the id of the user that was modified
"""
@app.route('/update_user/<id>', methods = ['PUT'])
def update_user(id):
	from database import User
	user = User.query.filter_by(id=id).first()
	if user:
		schem = UserSchema()
		#test if the input json is well formated
		if schem.validate(request.get_json(force=True), partial=True):
			return jsonify(schem.validate(request.get_json(force=True),partial=True))
		else:		
			new_user = schem.load(request.get_json(force=True), partial = True)			
			dico = (UserSchema().dump(new_user))
			#we discard all fields that are not specified
			dico = {key: val for key, val in dico.items() if (val is not None and key != "token")}
			#update all specified fields
			for key, val in dico.items():
				setattr(user, key,val)
			db.session.commit()
			return jsonify({'user_id' : user.id})
	else:
		abort(400)

"""
Entry point of the program
"""

if __name__ == '__main__':
	app.run(debug=True)