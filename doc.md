# Documentation for the RealEstate API

This documentation was NOT automatically generated, please update it along ith the main

## '/search/<city>', methods = ['GET']
Search enpoint, the name of the city is transmitted in a GET request

Returns all estate located in the given city, as JSON

## '/estate/<id>', methods = ['GET']
Get a specific estate by id

Returns a JSON containing all information on the id

## '/add_estate', methods = ['POST']
Add estate enpoint, the parameters are transmitted in a POST request
I assume here that a user must be registered - i.e. have a token - to add an estate
Expected format is json, required fields are name, re_type, city. Other possible fields are: description and rooms. 
Rooms need to be an array of rooms with each room defined as a JSON with required field "name" and optionnal field"description"

Returns estate id

## '/delete_estate/<id>', methods = ['DELETE']
Delete estate enpoint, the parameters are transmitted in a DELETE request
Only the owner of the estate can delete it, you need to specify a token in the json body

Returns true on success

## '/update_estate/<id>', methods = ['PUT']
Update estate enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
WARNING : the rooms field will be discarded, please use update_room, add_room or delete_room to update the rooms
This is meant to avoid having to specify all existing room
Expected format is json, the only required field is "token", every other field supplied with a not None value will be updated

Returns the id of the modified estate

## '/add_room', methods = ['POST']
Add a room to estate id with given name and description 
If estate_id does not match with an actual estate, will not add a room
Expected format is JSON, required fields are "name" and "token", optionnal field is "description"
returns the id of the room created

## '/update_room/<id>', methods = ['PUT']
Update user enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
Expected format is json, with the owner "token" field required. Optionnal fields are "name" and "description"

Returns the id of the user that was modified

## '/register', methods = ['POST']
"""
User registration enpoint, the parameters are transmitted in a POST request
Expected format is json, no fields are required, optionnal fields are "name", "surname", "bday" - with format '%d-%m-%Y'

Returns a token associated to the user - for simplicity sake, these token do not expire 
This might not be safe in a prod environnement, as the token is stored in plain text, but it will be used for symplicty
For a more traditionnal backend, I would use flask-login and sessions to restrict the access to certains users for a given set of endpoints
But this would not be stateless anymore

## '/update_user/<id>', methods = ['PUT']
Update user enpoint, the parameters are transmitted in a PUT request, update the specified parameters for the given id
I assume that everyone can update everyone's user info - except token ofc; but the same process as update_estate to limit to specific user could easily be implemented
Expected format is json, with no required field, and optionnal fields "name" and "description"

Returns the id of the user that was modified


