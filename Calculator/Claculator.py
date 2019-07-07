from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)


def checkdata(fxn, data):
    if fxn in ["add","sub","mul"]:
        if 'x' not in data or 'y' not in data:
            return 300
        else:
            return 200
    else:
        if fxn == "div":
            if ('x' not in data or 'y' not in data) and data['y'] == 0:
                return 300
            else:
                return 200

class add(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkdata("add", data)
        if status_code != 200:
            return jsonify({"Error":"Check for parameters", "Status Code":"300, Failure"})
        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        ret_json = { "Sum":ret, "Staus":200}
        return jsonify(ret_json)
    def get(self):
        msg = {"messge":"Thank you for calling this API, please post the values of x and y."}
        return jsonify(msg)


class sub(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkdata("sub", data)
        if status_code != 200:
            return jsonify({"Error":"Check for parameters", "Status Code":"300, Failure"})
        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x-y
        ret_json = { "sub":ret, "Staus":200}
        return jsonify(ret_json)


class mul(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkdata("mul", data)
        if status_code != 200:
            return jsonify({"Error":"Check for parameters", "Status Code":"300, Failure"})
        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        ret = x*y
        ret_json = { "mul":ret, "Staus":200}
        return jsonify(ret_json)

class div(Resource):
    def post(self):
        data = request.get_json()
        status_code = checkdata("div", data)
        if status_code != 200:
            return jsonify({"Error":"Check for parameters and 0 div error", "Status Code":"300, Failure"})
        x = data["x"]
        y = data["y"]
        x = int(x)
        y = int(y)
        if y == 0:
            return jsonify({"Error":"Cannot divide by 0", "Status Code":"300, Failure"})
        ret = (x*1.0)/y
        ret_json = { "div":ret, "Staus":200}
        return jsonify(ret_json)


#Channel the request to that perticular function 
api.add_resource(add, "/add")
api.add_resource(sub, "/sub")
api.add_resource(mul, "/mul")
api.add_resource(div, "/div")

# This routes to the HomePage
@app.route("/")
def hello():
    return "Hello World!!"

if __name__=="__main__":
    app.run(host="0.0.0.0")
