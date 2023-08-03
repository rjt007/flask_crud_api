from pymongo import MongoClient
import os
import certifi
ca = certifi.where()


DATABASE_URI = os.getenv("DATABASE_URI")

def connectDB():
    try:
        client = MongoClient(DATABASE_URI, tlsCAFile=ca)
        db = client.company
        return db
    except:
        print("Error! Cannot connect to db..")