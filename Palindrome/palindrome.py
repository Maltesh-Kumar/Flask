from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class palindrome(Resource):
    def post(self):
        data = request.get_json()

        n = data["number"]
        temp=n
        rev=0
        while(n>0):
    	    dig=n%10
    	    rev=rev*10+dig
    	    n=n//10
        if(temp==rev):
    	    ret_json = { "Result":"The number is a palindrome!", "Staus":200}
        else:
    	    ret_json = { "Result":"The number is NOT a palindrome!", "Staus":200}
        return jsonify(ret_json)





    def get(self):
        msg = {"messge":"Thank you for calling this API, please post the values of x and y."}
        return jsonify(msg)



#Channel the request to that perticular function
api.add_resource(palindrome, "/palindrome")


# This routes to the HomePage
@app.route("/")
def hello():
    return "Hello World!!"

if __name__=="__main__":
    app.run(host="0.0.0.0")
