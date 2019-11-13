#!/usr/bin/env python


from flask import request, jsonify
from sqlalchemy.sql import func
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, Schema
from database import  UserSchema, EstateSchema, RoomSchema

import config

from config import db, app


app = config.app
db.create_all()

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
	print(estates_schemas.dump(estates))
	return jsonify(estates_schemas.dump(estates))


"""
Add estate enpoint, the parameters are transmitted in a POST request
Expected format is

Returns estate id
"""
@app.route('/add_estate', methods = ['POST'])
def add_estate():
	schem = EstateSchema()
	#test if the input json is well formated
	if schem.validate(request.get_json(force=True)):
		return jsonify(schem.validate(request.get_json(force=True)))
	else:		
		new_estate = schem.load(request.get_json(force=True))
		#will generate room objects too
		db.session.add(new_estate)
		db.session.commit()
		return jsonify({'estate_id' : new_estate.id})
"""
Update estate enpoint, the parameters are transmitted in a POST request
Separate endpoint from add_estate to avoid accidental overriding of a real estate
Expected format is


Returns the new representation of the estate as JSON ?
"""
@app.route('/update_estate', methods = ['POST'])
def update_estate():
	if not request.json or not 'id' in request.json:
		abort(400)

"""
User registration enpoint, the parameters are transmitted in a POST request
Expected format is


Returns the new representation of the user as JSON ?
"""
@app.route('/register', methods = ['POST'])
def register():
	if not request.json:
		abort(400)


"""
Update user infos enpoint, the parameters are transmitted in a POST request
Expected format is


Returns the new representation of the user as JSON ?
"""
@app.route('/update_user', methods = ['POST'])
def update_user():
	if not request.json:
		abort(400)


"""
Entry point of the program
"""

if __name__ == '__main__':
	app.run(debug=True)