from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import app.db_config as database


app = Flask(__name__) #declarates the statement to running the app
api = Api(app) # declarates the API as variable to then to establishing the endpoints
CORS(app) #

''' Lines for the JSON options to manage endpoints in insomnia (line 12 to 44)'''
#generates the argument for the deployment of the POST endpoint
post_students_args = reqparse.RequestParser()

#establishes the POST variables with their type, error mesaage and requested type (15 to 27)
post_students_args.add_argument(
    "id", type=int, help="ERROR id value needs to be an integer", required=True)
post_students_args.add_argument(
    "first_name", type=str, help="ERROR first_name is required", required=True)
post_students_args.add_argument( 
    "last_name", type=str, help="ERROR last_name is required", required=True)
post_students_args.add_argument(
    "image", type=str, help="ERROR you need to add the image url", required=True)
post_students_args.add_argument(
    "group", type=str, required=False)
post_students_args.add_argument(
    "career", type=str, required=False)

#generates the argument for the deployment of the PATCH endpoint
patch_students_args = reqparse.RequestParser()

#establishes the POST variables with their type, error mesaage and requested type (33 to 44)
patch_students_args.add_argument(
    "id", type=int, help="ERROR id value needs to be an integer", required=False)
patch_students_args.add_argument(
    "first_name", type=str, help="ERROR first_name is required", required=False)
patch_students_args.add_argument(
    "last_name", type=str, help="ERROR last_name is required", required=False)
patch_students_args.add_argument(
    "image", type=str, help="ERROR you need to add the image url", required=False)
patch_students_args.add_argument(
    "group", type=str, required=False)
patch_students_args.add_argument(
    "career", type=str, required=False)

#class made for testing the connection with the db
class Test(Resource):

    def get(self):
        return jsonify({"message":"You are connected"})

#class to GET all students
class Students(Resource):
    #function to GET all students
    def get(self):
        response = list(database.db.students.find()) #finds a list of all the students as a variable
        students = [] # declares an empty list/array
        # cicle to deletes every mongo _id from all students (lines 59 - 61)
        for student in response: 
            del student['_id']
            students.append(student) # adds the new results without _id
        return jsonify({'results':students}) # returns a jsonified dictionary with the results

#class to manage endpoints for a single student
class Student(Resource):
    #function to GET a specific student
    def get(self, id):
        response = database.db.students.find_one({'id':id}) #finds one student as a variable
        del response['_id'] #deletes every mongo _id from all students
        return jsonify(response) #returns a jsonified response

    #function to POST a new student
    def post(self):
        args = post_students_args.parse_args() #gets the arguments at line 13
        self.abort_if_id_exist(args['id']) #aborts the operation if the id already exists
        #inserts one student with the help of the json inputs at lines 15 to 27 (lines 77 to 84)
        database.db.students.insert_one({ 
            'id': args['id'],
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'image': args['image'],
            'group': args['group'],
            'career': args['career'],
        })
        return jsonify(args) #returns a jsonified response

    #function to PUT(update) a specific student
    def put(self, id): 
        args = post_students_args.parse_args() #gets the arguments at line 13
        self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        #updates students' with the help of the json inputs at lines 15 to 27 (lines 92 to 101)
        database.db.students.update_one(
            {'id':id},
            {'$set':{
               'id': args['id'],
                'first_name': args['first_name'],
                'last_name': args['last_name'],
                'image': args['image'],
                'group': args['group'],
                'career': args['career'], 
            }}
        )
        return jsonify(args) #returns a jsonified response

    #function to PATCH (update one) data from the student
    def patch(self, id):
        student = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        args = patch_students_args.parse_args() #gets the arguments at line 30
        #updates one specific students' data with the help of the json inputs at lines 33 to 44 (lines 110 to 120)
        database.db.students.update_one(
            {'id':id},
            {'$set':{
                'id': args['id'] or student['id'],
                'first_name': args['first_name'] or student['first_name'],
                'last_name': args['last_name'] or student['last_name'],
                'image': args['image'] or student['image'],
                'group': args['group'] or student['group'],
                'career': args['career'] or student['career'], 
            }
        })

        student = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        del student['_id'] #deletes the mongo _id of the student
        return jsonify(student) #returns a jsonified response
    
    #function to DELETE a specific student
    def delete(self, id):
        student = self.abort_if_not_exist(id) #aborts the operation if the id do not exists
        database.db.students.delete_one({'id':id}) #deletes by getting the id
        del student['_id'] #deletes the mongo _id of the student
        return jsonify({'deleted student': student}) #returns a jsonified response

    #function that finds an id that exists already; 
    #aborts the operation and returns jsonfied message (line 134 to 138) 
    def abort_if_id_exist(self, id):
        if database.db.students.find_one({'id':id}):
            abort(
                jsonify({'error':{'406': f"The student with the id: {id} already exist"}}))

    #function that searches an existent id; 
    #aborts the operation and returns a jsonfied message or process the operation (line 142 to 148) 
    def abort_if_not_exist(self, id):
        student = database.db.students.find_one({'id':id})
        if not student:
            abort(
                jsonify({'error':{'404': f"The student with the id: {id} not found"}}))
        else:
            return student

#defines the endpoints for the url to use the API by doing the classes' operations (lines 151 to 153)
api.add_resource(Test,'/test/')
api.add_resource(Students,'/students/')
api.add_resource(Student, '/student/', '/student/<int:id>/')

#runs the app for a local server
if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)