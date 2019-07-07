from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import json

app = Flask(__name__)
api = Api(app)

#connecting it to MongoDB ATLAS
client = MongoClient("mongodb+srv://<username>:<password>@mongo-1-emgh2.mongodb.net/test?retryWrites=true&w=majority") 
db = client.sentencedatabase
users = db["user"]


class register(Resource):
    def post(self):
        #GET POSTED DATA FROM USER
        posteddata = request.get_json()

        #GET DATA
        username = posteddata["username"]
        password = posteddata["password"]

        #STORIN PASSWORD IN FORM OF HASH
        hashpwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #STORING USERNAME AND PASSWD INTO DATABASE
        users.insert(
        {
        "username": username,
        "password": hashpwd,
        "sentence": [],
        "tokens":5
        }
        )

        #RETURNING BACK TO USER
        ret = {
        "status":200,
        "message": "Execution Successful"
        }

        return jsonify(ret)


def verify_user(username, password):
    hashedpwd = users.find(
    {
    "username":username
    }
    )[0]["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashedpwd)==hashedpwd:
        return True
    else:
        return False

def verify_tok(username):
    n_tok = users.find(
    {
    "username":username
    }
    )[0]["tokens"]
    return n_tok


class store(Resource):
    def post(self):
        #GET THE POSTED DATA
        posteddata = request.get_json()

        #READING THE DATA
        username = posteddata["username"]
        password = posteddata["password"]
        sentence = posteddata["sentence"]

        #VERIFY USERNAME AND PASSWD MATCH
        correct_match = verify_user(username, password)

        if not correct_match:
            ret_match = {
            "status":302,
            "messgae":"match not found"
            }
            return jsonify(ret_match)

        #VERIFY BALANCE OF TOKENS
        '''
        verify_bal = verify_tok(username)
        if verify_bal < 1:
            ret_token = {
            "status":301,
            "message":"out of balance"
            }
            return jsonify(ret_token)
        '''



        #IF VERIFIED STORE SENTENCE AND RETURN 200 OK AND REDUCE 1 TOKEN
        users.update({"username":username},{"$push":{"sentence":sentence}})

        #users.update({"username":username},{"$set":{"tokens":verify_bal-1}})

        ret_succ = {
        "status":200,
        "message":"sentence saved successful"
        }
        return jsonify(ret_succ)




class get(Resource):
    def post(self):
        posteddata = request.get_json()
        username = posteddata["username"]
        password = posteddata["password"]

        correct_match = verify_user(username, password)
        if not correct_match:
            ret_match = {
            "status":302,
            "messgae":"match not found"
            }
            return jsonify(ret_match)

        verify_bal = verify_tok(username)
        if verify_bal < 1:
            ret_token = {
            "status":301,
            "message":"out of balance"
            }
            return jsonify(ret_token)


        users.update({
        "username":username
        },{
        "$set":{
                "tokens":verify_bal-1
                }
        })


        res = users.find({"username":username})[0]['sentence']


        ret = {
        "sentence":res,
        "balance remaining":verify_bal,
        "status":200
        }

        return jsonify(ret)


def userexists(username):
    if users.find({"username":username}).count() == 0:
        return False
    else:
        return True


def counttoken(username):
    tokens = users.find({"username":username})[0]['tokens']
    return tokens



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
        users.update({"username":username},{"$set":{"tokens":refill+currenttoken}})
        totaltoken = counttoken(username)

        ret = {
        "status":200,
        "previous-balance":currenttoken,
        "current-balance":totaltoken,
        "message":"token re-fill successful"
        }
        return jsonify(ret)


api.add_resource(register, '/register')
api.add_resource(store, '/store')
api.add_resource(get, '/get')
api.add_resource(refill,'/refill')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
