# Assault API

The main purpose of this API is to store the information about the location and details of 
assaults and crimes in Chihuahua Chihuahua. This information will be utilized in conjunction
with Google Maps API, the idea is to create a Map where we can display fictional crime events
in our APP.


## Features

- Provides detail location where crimes were commited
- Provides the user the type of crime that was commited
- Provides the information ordered as a list with an ID each crime

## Parameters 

- id: as unique integer
- coordinates: as a dictionary for the latitude and the longitude
    - x: is a float number that represents the longitude
    - y: is a float number that represents the latitude
- crime_type: is a string with the type of crime that was commmited

## Results

The output results of this API are JSON files for the
user to implement this information on a project where 
the user wants to know specific location of crimes 
commited and the type of crimes that were commited.

## Endpoints

This API only has 2 endpoints, the POST and PATCH


- PATCH: this endpoint allow us to make changes on 
the information of the API
- POST: This endpoint allow us to add more data into 
the API

## Requirements
- aniso8601==9.0.1 || Date converter
- click==8.0.4 || Makes Command Line Interfaces better
- colorama==0.4.4 || produce colored terminal text 
- dnspython==2.2.1 || DNS toolkit for Python
- Flask==2.0.3 || web framework
- Flask-Cors==3.0.10 || flask extention for handling CROS
- Flask-PyMongo==2.3.0 || pymongo database extension from flask
- Flask-RESTful==0.3.9 || Adds support for quickly building REST APIs
- gunicorn==20.1.0 || HTTP server
- itsdangerous==2.1.2 || Security managment of data
- Jinja2==3.1.0 || templating engine
- MarkupSafe==2.1.1 || Implements a text object that escapes character
- pymongo==4.0.2 || mongodb extension for python
- python-dotenv==0.19.2 || Reads key-value pairs from a .env file
- pytz==2022.1 || Is an interface to the IANA database
- six==1.16.0 || Provides utility functions for smoothing between py versions
- Werkzeug==2.0.3 || Comprehensive WSGI web application library


## Deployment
MongoDB was utilized to test our database connections and all the required information before deploying the API to the web. 

<img src='https://www.bacula.lat/wp-content/uploads/2020/02/MongoDB_Logo_FullColorBlack_RGB-4td3yuxzjs.png' width="300">

We utilized Heroku to Deploy the API.

<img src='https://tudip.com/wp-content/uploads/2018/06/1_9wOLuKSjCIAqSX_K8O0PKQ-800x302.png' width="300">

The process of deployment was done through cmder with the implementation of heroku and git. 

<img src='https://i0.wp.com/colaboratorio.net/wp-content/uploads/2017/01/git_000.jpg?fit=1200%2C600&ssl=1' width="300">

## Screenshots / API functioning.

<img src='https://s7.gifyu.com/images/Captura47.png'>
<img src='https://s7.gifyu.com/images/Screenshot-2022-03-30-212248.jpg'>

## Authors

- [Fabian Galarza](https://github.com/AetherFabian)
- [Joshua Aviles](https://github.com/JoshuaAv07)
- [Gustavo Valladolid](https://github.com/gusvalladolid)
- [Carlos Salazar](https://github.com/CarlosSSC)
- [Jonatan Rico](https://github.com/Jocarico)
- [Daniel Flores](https://github.com/Poncho1424)

