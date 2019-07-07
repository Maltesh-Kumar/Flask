from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

#connecting it to MongoDB ATLAS
client = MongoClient("mongodb+srv://<username>:<password>@mongo-1-emgh2.mongodb.net/test?retryWrites=true&w=majority") 
db = client.similarityDB

users = db["users"]


def userexists(username):
    if users.find({"username":username}).count() == 0:
        return False
    else:
        return True

class register(Resource):
    def post(self):
        posteddata = request.get_json()
        username = posteddata["username"]
        password = posteddata["password"]

        #CHECKING IF USER ALREADY EXISTS
        if userexists(username):
            ret = {
            "status":301,
            "message":"username already exists"
            }
            return jsonify(ret)

        hashedpwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
        "username":username,
        "password":hashedpwd,
        "token":5
        })

        ret = {
        "status":200,
        "message":"sucessfully registered to API"
        }

        return jsonify(ret)



def counttoken(username):
    tokens = users.find({"username":username})[0]['token']
    return tokens



def verifypwd(username, password):
    if not userexists(username):
        return False
    else:
        hashedpwd = users.find({"username":username})[0]['password']
        if bcrypt.hashpw(password.encode('utf8'), hashedpwd)==hashedpwd:
            return True
        else:
            return False


class detect(Resource):
    def post(self):
        posteddata = request.get_json()
        username = posteddata["username"]
        password = posteddata["password"]
        text1 = posteddata["text-1"]
        text2 = posteddata["text-2"]

        if not userexists(username):
            ret = {
            "status":301,
            "message":"invalid username"
            }
            return jsonify(ret)

        correctpwd = verifypwd(username, password)
        if not correctpwd:
            ret = {
            "status":302,
            "message":"invalid password"
            }
            return jsonify(ret)

        ntok = counttoken(username)
        if ntok < 1:
            ret = {
            "status":303,
            "message":"out of tokens... please refill"
            }
            return jsonify(ret)

        #SPACY MODEL
        nlp = spacy.load('en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)

        #RATIO OF SIMILARITY BETWEEN 2 TEXT
        ratio = text1.similarity(text2)

        disptoken = users.find({"username":username})[0]['token']

        ret = {
        "status":200,
        "similarity":ratio,
        "token-left":disptoken,
        "result":"result calculated..!!"
        }

        ct = counttoken(username)
        users.update({"username":username},{"$set":{"token":ct-1}})

        return jsonify(ret)


class refill(Resource):
    def post(self):
        posteddata = request.get_json()
        username = posteddata["username"]
        password = posteddata["otp"]
        refill = posteddata["refill-amt"]

        if not userexists(username):
            ret = {
            "status":301,
            "message":"user not found"
            }
            return jsonify(ret)

        #THIS IS BASICALLY IMPLEMENTED IF A USER WANTS MORE TOKENS HE CAN RECHARGE AND HE GETS AN OTP
        #ASSUMING OTP IS "1234" AS IF HAVE NOT IMPLEMENTED ANY LIVE PAYMENT VALIDATION FOR TOKEN REFILL
        otp_pass = 1234
        if password != otp_pass:
            ret = {
            "status":304,
            "message":"incorrect password"
            }
            return jsonify(ret)

        currenttoken = counttoken(username)
        users.update({"username":username},{"$set":{"token":refill+currenttoken}})
        totaltoken = counttoken(username)

        ret = {
        "status":200,
        "previous-balance":currenttoken,
        "current-balance":totaltoken,
        "message":"token re-fill successful"
        }
        return jsonify(ret)


api.add_resource(register,'/register')
api.add_resource(refill,'/refill')
api.add_resource(detect,'/detect')


if __name__ == "__main__":
    app.run(host="0.0.0.0")
