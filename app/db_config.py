from flask_pymongo import pymongo
import os

#next three lines brings the data from .env
DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

#connects to the mongo's database that ir created for the project
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@assault.on5ch.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")

#declares the database connection as variable
db = client.assault

#db = client.students