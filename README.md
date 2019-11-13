# RealEstate API Using Flask

This repo contains the implementation for a real estate service Rest API, implemented using Flask and SQLAlchemy 

## Installation & Usage

This project was build for Python3.7 - Python 3.6 should be supported as well -
Usage of a virtualenv is recommended, all dependencies can be found in [requirements.txt](requirements.txt)

The server is currently configured for a localhost usage, see e.g [official Flask documentation](http://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/?highlight=apache#configuring-apache) to set it up on production

Current server implementation can be launched using './main.py'
Warning : the database file is not cleaned at startup, this is an implementation choice

For a list of all enpoints, see the [doc](doc.md). 
Some additionnal enpoints could be useful, but their implementation would be pretty straight forward and close to existing endpoints

This api uses Flask,  SQLAlchemy and Marshmallow for json deserialization, making the code light and adaptable
So adding features or modifying existing codebase would not be a problem
## Integration Tests

You can run integration tests using [tests.py](tests.py), make sure that you delete the database and restart the server first
You could run the tests - and additionnal tests outside of the virtual env, the only dependance for the tests is [requests](https://pypi.org/project/requests/2.7.0/)

## Bugs

If you find a bug, please report it using the issue tab of this github, or contact me at louis.morin.pro@gmail.com
