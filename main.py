#!/usr/bin/env python
from flask import Flask
from flask import request, jsonify
from sqlalchemy.sql import func



app = Flask(__name__)

@app.route('/')
def index():
    return "This is a RESTful API, please use the appropriate endpoints"

@app.route('/search/<city>', methods = ['GET'])
def search(city):
	return jsonify({'TODO': city})


@app.route('/update_estate', methods = ['POST'])
def update_estate():
	if not request.json or not 'id' in request.json:
		abort(400)

@app.route('/register', methods = ['POST'])
def register():
	if not request.json:
		abort(400)

@app.route('/update_user', methods = ['POST'])
def update_user():
	if not request.json:
		abort(400)




if __name__ == '__main__':
	from database import db
	print("creating database")
	db.create_all()
	print("database created")
	app.run(debug=True)