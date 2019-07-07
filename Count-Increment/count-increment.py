from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

#connecting it to MongoDB ATLAS
client = MongoClient("mongodb+srv://<username>:<password>@mongo-1-emgh2.mongodb.net/test?retryWrites=true&w=majority") 


db = client.aNewdb  #aNewdb is database name
frequency = db["refresh"] #building collection frequency in db and frequency variable is used to denote the database

#usernum is used to check no. of users
frequency.insert(
{
'no_of_refresh_time':0
}
)

class visit(Resource):
     def get(self):
         prev_num = frequency.find()[0]['no_of_refresh_time']
         new_num = prev_num + 1
         frequency.update({},{"$set":{'no_of_refresh_time':new_num}})
         return str("Refresh Time : "+str(new_num))


api.add_resource(visit, "/visit")


@app.route("/")
def hello():
    return "Hello World!!"

if __name__=="__main__":
    app.run(host="0.0.0.0")
