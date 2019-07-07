from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import datetime

app = Flask(__name__)
api = Api(app)


class next_date(Resource):
    def post(self):
        data = request.get_json()

        inp_date = data["date"]  #SHOULD RECEIVE IN DD MM YY  ---> Ex: 16 Jan 2011
        d = datetime.datetime.strptime(inp_date,"%d %b %Y")
        day = d.day
        month = d.month
        year = d.year
        #CHECK FOR LEAP YEAR
        if (year % 400 == 0):
    	    leap_year = True
        elif (year % 100 == 0):
    	    leap_year = False
        elif (year % 4 == 0):
    	    leap_year = True
        else:
    	    leap_year = False

        if month in (1, 3, 5, 7, 8, 10, 12):
    	    month_length = 31
        elif month == 2:
    	    if leap_year:
                month_length = 29
    	    else:
                month_length = 28
        else:
    	    month_length = 30

        if day < month_length:
    	    day += 1
        else:
    	    day = 1
    	    if month == 12:
                month = 1
                year += 1
    	    else:
                month += 1


        if leap_year:
            ret_json = { "Result":"The next date is %d-%d-%d."%(year, month, day),"Leap Year":True, "Staus":200}
        else:
            ret_json = { "Result":"The next date is %d-%d-%d."%(year, month, day),"Leap Year":False, "Staus":200}
        return jsonify(ret_json)




    def get(self):
        msg = {"messge":"Thank you for calling this API, please post the values of x and y."}
        return jsonify(msg)



#Channel the request to that perticular function
api.add_resource(next_date, "/next")


# This routes to the HomePage
@app.route("/")
def hello():
    return "Hello World!!"

if __name__=="__main__":
    app.run(host="0.0.0.0")
