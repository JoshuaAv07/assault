from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import app.db_config as database

app = Flask(__name__) #declarates the statement to running the app
api = Api(app) # declarates the API as variable to then to establishing the endpoints
CORS(app) # 

''' Lines for the JSON options to manage endpoints in insomnia (line 12 to )'''
#generates the argument for the deployment of the POST endpoint
post_assaults_args = reqparse.RequestParser()

#establishes the POST variables with their type, error mesaage and requested type (15 to 20)

post_assaults_args.add_argument(
    "crime_type", type=str, help="ERROR crime_type is required", required=True)

#generates the argument for the deployment of the PATCH endpoint
patch_assaults_args = reqparse.RequestParser()

#establishes the POST variables with their type, error mesaage and requested type (25 to 31)

patch_assaults_args.add_argument(
    "crime_type", type=str, help="ERROR crime_type is required", required=False)

#class made for testing the connection with the db
class Test(Resource):
    def get(self):
        return jsonify({"message":"You are connected"})

#class to GET all students
class Assaults(Resource):
    #function to GET all students
    def get(self):
        response = list(database.db.assault.find()) #finds a list of all the students as a variable
        assaults = [] # declares an empty list/array
        # cicle to deletes every mongo _id from all students (lines 59 - 61)
        for assault in response: 
            del assault['_id']
            assaults.append(assault) # adds the new results without _id
        return jsonify({'results':assaults}) # returns a jsonified dictionary with the results

#class to manage endpoints for a single student
class Assault(Resource):
    #function to GET a specific student
    def get(self, id):
        response = database.db.assault.find_one({'id':id}) #finds one student as a variable
        del response['_id'] #deletes every mongo _id from all students
        return jsonify(response) #returns a jsonified response

    #function to POST a new student
    def post(self):
        coordinates = request.json["coordinates"]
        args = post_assaults_args.parse_args() #gets the arguments at line 13
        id = self.get_next_id()
        #inserts one student with the help of the json inputs at lines 15 to 27 (lines 77 to 84)
        
        self.validate_coordinates(request.json["coordinates"])
        
        database.db.assault.insert_one({ 
            'id': id,
            'crime_type': args['crime_type'],
            'coordinates':{
                "x": coordinates["x"],
                "y": coordinates["y"]
            }
        })
        return self.get(id) #returns a jsonified response

    #function to PUT(update) a specific student
    def put(self, id): 
        coordinates = request.json["coordinates"]
        args = post_assaults_args.parse_args() #gets the arguments at line 13
        self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        self.validate_coordinates(request.json["coordinates"])
        #updates students' with the help of the json inputs at lines 15 to 27 (lines 92 to 101)
        database.db.assault.update_one(
            {'id':id},
            {'$set':{
                'crime_type': args['crime_type'],
                'coordinates':{
                    "x": coordinates["x"],
                    "y": coordinates["y"]
                }
            }}
        )
        return self.get(id) #returns a jsonified response

    #function to PATCH (update one) data from the student
    def patch(self, id):
        coordinates = {}
        try:
            coordinates = request.json["coordinates"]
            self.validate_coordinates(request.json["coordinates"])
        except:
            pass
        
        
        assault = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        args = patch_assaults_args.parse_args() #gets the arguments at line 30
        #updates one specific students' data with the help of the json inputs at lines 33 to 44 (lines 110 to 120)
        try:
            x = coordinates["x"]
        except:
            x = assault["coordinates"]["x"]
        try:
            y = coordinates["y"]
        except:
            y = assault["coordinates"]["y"]
        database.db.assault.update_one(
            {'id':id},
            {'$set':{
                'crime_type': args['crime_type'] or assault['crime_type'],
                'coordinates':{
                    "x": x,
                    "y": y
                }
            }
        })

        assault = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        del assault['_id'] #deletes the mongo _id of the student
        return self.get(id)  #returns a jsonified response
    
    #function to DELETE a specific student
    def delete(self, id):
        assault = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        database.db.assault.delete_one({'id':id}) #deletes by getting the id
        del assault['_id'] #deletes the mongo _id of the student
        return jsonify({'deleted crime': assault}) #returns a jsonified response

    #function that finds an id that exists already; 
    #aborts the operation and returns jsonfied message (line 134 to 138) 
    def abort_if_id_exist(self, id):
        if database.db.assault.find_one({'id':id}):
            abort(
                jsonify({'error':{'406': f"The crime with the id: {id} already exist"}}))

    #function that searches an existent id; 
    #aborts the operation and returns a jsonfied message or process the operation (line 142 to 148) 
    def abort_if_not_exist(self, id):
        assault = database.db.assault.find_one({'id':id})
        if not assault:
            abort(
                jsonify({'error':{'404': f"The crime with the id: {id} not found"}}))
        else:
            return assault
        
    def validate_coordinates(self,coordinates):
        if not isinstance(coordinates["x"],str) and not isinstance(coordinates["y"],str):
            abort(jsonify({'error':"Coordinates must be and string"}))
        if not coordinates["x"] or not coordinates["y"]:
            abort(jsonify({'error':"ERROR Coordinates is required"}))
            
    def get_next_id(self):
        response = list(database.db.assault.find()) #finds a list of all the students as a variable
        if response:
            assaults = [] # declares an empty list/array
            # cicle to deletes every mongo _id from all students (lines 59 - 61)
            for assault in response: 
                del assault['_id']
                assaults.append(assault) # adds the new results without _id

            assaults = assaults[::-1]
            
            return assaults[0]["id"] + 1 # returns a jsonified dictionary with the results
            
        else:
            assaults = 1
            return assaults
            

#defines the endpoints for the url to use the API by doing the classes' operations (lines 151 to 153)
api.add_resource(Test,'/test/')
api.add_resource(Assaults,'/assaults/')
api.add_resource(Assault, '/assault/', '/assault/<int:id>/')

#runs the app for a local server
if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)
