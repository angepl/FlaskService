from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import jwt #needs PyJWT installation
import datetime
from functools import wraps
from bson.objectid import ObjectId

#Connect to our local MongoDB
client = MongoClient('mongodb://mongodb:27017/')

#Choose database and collections
db = client['DigitalAirlines']
users = db['users']
flights = db['flights']
bookings = db['bookings']

#Initiate Flask App
app = Flask(__name__)

#create secret key for jwt authentication
app.config["SECRET_KEY"] = "!nfoSys2023"



#authentication mechanism
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #get token argument
        token = request.args.get("token")

        if not token:
            return Response("Endpoint needs authentication token", status=401)
        
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
           return Response("Invalid token", status=403)
        
        return f(*args, **kwargs)
    return decorated



#endpoint for new registry
@app.route('/newRegistry', methods=['POST'])
def new_registry():
    #Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500)
    if not "name" in data or not "surname" in data or not "email" in data or not "password" in data or not "dateOfBirth" in data or not "country" in data or not "passport" in data:
        return Response("Information incomplete",status=500)
    else:
        #check if there is already a user with this email
        if users.count_documents({"email":data["email"]}) == 0: 
            #declare record details - this endpoint can only insert a simple user in the database (role=simpleUser)
            user = {"name": data["name"], "surname": data["surname"], "email": data["email"], "password": data["password"], "dateOfBirth": data["dateOfBirth"], "country": data["country"], "passport": data["passport"], "role": "simpleUser"} 
            #insert user
            users.insert_one(user)
            return Response("User was added to the database",status=200) 
        else:
            return Response("A user with the given email already exists",status=200)



#endpoint for login
@app.route('/login', methods=['POST'])
def login():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500)
    if not "email" in data or not "password" in data:
        return Response("Information incomplete. Try again",status=500)
    else:
        #check if there is already a user with this email and password
        user = users.find_one({"email":data["email"], "password":data["password"]}) 
        if user is None:
            return Response("No user with these credentials. Try again",status=403)
        else:
            #if there is a user with these credentials, create and return an authentication token (token is valid for 60 minutes)
            token = jwt.encode({"email": data["email"], "role":user["role"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config["SECRET_KEY"])
            return jsonify({"token": token})
            



#list where I will store tokens of users that have logged out (destroyed tokens)
blacklist = []

#endpoint for logout
@app.route('/logout', methods=['GET'])
#authentication required for this endpoint
@token_required
def logout():
    #get token argument
    token = request.args.get("token")
    #if the token has been destroyed (because of previous logout)
    if token in blacklist:
        return Response("Invalid token", status=403)
    #if the token is still valid
    else:
        #destroy it 
        blacklist.append(token)
        return Response("Successfull logout", status=200)




#------------ONLY ADMIN ENDPOINTS-------------

#endpoint to insert flight
@app.route("/insertFlight", methods=['POST'])
#authentication required for this endpoint
@token_required
def insert_flight():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin
    if raw["role"] != "admin":
        return Response("Access denied", status=403)

    #Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad json content",status=500)
    if not "from" in data or not "to" in data or not "date" in data or not "businessTickets" in data or not "businessPrice" in data or not "economyTickets" in data or not "economyPrice" in data:
        return Response("Information incomplete",status=500)
    else:
        #declare record details
        flight = {"from": data["from"], "to": data["to"], "date": data["date"], "businessTickets": data["businessTickets"], "businessPrice": data["businessPrice"], "economyTickets": data["economyTickets"], "economyPrice": data["economyPrice"]} 
        #insert flight
        flights.insert_one(flight)
        return Response("Flight was added to the database",status=200) 




#endpoint to update ticket price
@app.route("/updatePrice", methods=['PUT'])
#authentication required for this endpoint
@token_required
def update_price():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin
    if raw["role"] != "admin":
        return Response("Access denied", status=403)

    #Request JSON data
    data = None 
    try:
        #data has to include the _id (not the ObjectId - only the characters)
        data = json.loads(request.data)
    
        if not "_id" in data or (not "businessPrice" in data and not "economyPrice" in data):
            return Response("Information incomplete",status=500)
        elif flights.count_documents({"_id": ObjectId(data["_id"])}) == 0:
            return Response("No flight found", status=200)
        else:
            #update price
            if "businessPrice" in data and "economyPrice" in data:
                flights.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"businessPrice": data["businessPrice"], "economyPrice": data["economyPrice"]}})
            elif "businessPrice" in data:
                flights.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"businessPrice": data["businessPrice"]}})
            elif "economyPrice" in data:
                flights.update_one({"_id": ObjectId(data["_id"])}, {"$set": {"economyPrice": data["economyPrice"]}})
    except Exception as e:
        return Response("Bad json content",status=500)

    return Response("Flight price was updated",status=200) 




#enpoint for flight delete
@app.route("/deleteFlight", methods=['DELETE'])
#authentication required for this endpoint
@token_required
def delete_flight():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin
    if raw["role"] != "admin":
        return Response("Access denied", status=403)

    #Request JSON data
    data = None 
    try:
        #data has to include the _id (not the ObjectId - only the characters)
        data = json.loads(request.data)
    
        if not "_id" in data:
            return Response("Information incomplete",status=500)
        elif bookings.count_documents({"flightId": data["_id"]}) != 0:
            return Response("This flight has active bookings. Delete denied", status=200)
        else:
            #delete flight
            flights.delete_one({"_id": ObjectId(data["_id"])})
    except Exception as e:
        return Response("Bad json content",status=500)

    return Response("Flight sucessfully deleted",status=200) 




#-------------ΟΝLY SIMPLE USER ENDPOINTS--------------


#endpoint for ticket booking
@app.route("/ticketBooking", methods=['POST'])
#authentication required for this endpoint
@token_required
def ticket_booking():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "simpleUser":
        return Response("Access denied", status=403) 

    #Request JSON data
    data = None 

    try:
        data = json.loads(request.data)
        
        if not "flightId" in data or not "name" in data or not "surname" in data or not "passport" in data or not "dateOfBirth" in data or not "email" in data or not "ticketType" in data:
            return Response("Information incomplete",status=500)
        #check if ticketType has a valid value
        elif data["ticketType"] != "economy" and data["ticketType"] != "business":
            return Response("Ticket type must be either economy or business.", status=400)
        elif data["email"] != raw["email"]:
            return Response("The email does't belong to this account!", status=400)
        elif users.count_documents({"email":data["email"], "role":"simpleUser"}) == 0:
            return Response("No (simple) user with that email in the database", status=400)
        else:
            #declare record details
            booking = {"flightId": data["flightId"], "name": data["name"], "surname": data["surname"], "passport": data["passport"], "dateOfBirth": data["dateOfBirth"], "email": data["email"], "ticketType": data["ticketType"]} 
            #insert booking
            bookings.insert_one(booking)
            return Response("Booking was added to the database",status=200)
    
    except Exception as e:
        return Response("Bad json content",status=500)



#endpoint to show bookings of user
@app.route("/showBookings", methods=['GET'])
#authentication required for this endpoint
@token_required
def show_bookings():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "simpleUser":
        return Response("Access denied", status=403) 
    
    list = []
    
    #find bookings with user email
    results = bookings.find({"email": raw["email"]})

    #put results in a list
    for result in results:
        list.append({"_id":str(result["_id"]), "flightId": result["flightId"], "name":result["name"], "surname": result["surname"], "passport":result["passport"], "dateOfBirth":result["dateOfBirth"], "email": result["email"], "ticketType": result["ticketType"]})

    #return list in json format
    return jsonify(list)




#endpoint to show booking details by booking _id
@app.route("/showBookingDetails", methods=['POST'])
#authentication required for this endpoint
@token_required
def show_booking_details():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "simpleUser":
        return Response("Access denied", status=403) 

    #Request JSON data
    data = None 

    try:
        #data has to include the booking _id (not the ObjectId - only the characters)
        data = json.loads(request.data)
            
        if not "_id" in data:
            return Response("Information incomplete",status=500)
        else:
            #find booking with that id that belongs to this user
            booking = bookings.find_one({"_id": ObjectId(data["_id"]), "email":raw["email"]})
            #if there is no such booking
            if booking is None:
                return Response("There is no booking with that id for this account", status=200)
            else:
                #find the flight that belongs to this booking
                flight = flights.find_one({"_id": ObjectId(booking["flightId"])})
                #return booking details
                return jsonify({"from": flight["from"], "to": flight["to"], "date": flight["date"], "name": booking["name"], "surname": booking["surname"], "passport": booking["passport"], "dateOfBirth": booking["dateOfBirth"], "email": booking["email"], "ticketType": booking["ticketType"]})

    except Exception as e:
        return Response("Bad json content",status=500)




#enpoint for booking delete
@app.route("/deleteBooking", methods=['DELETE'])
#authentication required for this endpoint
@token_required
def delete_booking():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "simpleUser":
        return Response("Access denied", status=403)

    #Request JSON data
    data = None 
    try:
        #data has to include the booking _id (not the ObjectId - only the characters)
        data = json.loads(request.data)
    
        if not "_id" in data:
            return Response("Information incomplete",status=500)
        else:
            #check if there is a booking with that id for this account
            booking = bookings.find_one({"_id": ObjectId(data["_id"]), "email": raw["email"]})
            #if there is no such booking
            if booking is None:
                return Response("There is no booking with that id for this account", status=200)
            else:
                bookings.delete_one({"_id": ObjectId(data["_id"])})
                return Response("Booking sucessfully canceled",status=200) 
    
    except Exception as e:
        return Response("Bad json content",status=500)




#enpoint to delete acount
@app.route("/deleteAccount", methods=['DELETE'])
#authentication required for this endpoint
@token_required
def delete_account():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "simpleUser":
        return Response("Access denied", status=403)

    #delete user
    users.delete_one({"email": raw["email"]})
    return Response("Account sucessfully deleted",status=200) 



    


#-------------ADMIN AND SIMPLE USER ENDPOINTS--------------


#endpoint for flight search
@app.route("/searchFlight", methods=['POST'])
#authentication required for this endpoint
@token_required
def search_flight():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "admin" and raw["role"] != "simpleUser":
        return Response("Access denied", status=403)

    #Request JSON data
    data = None 

    try:
        data = json.loads(request.data)

        list = []
            
        if data: #if data exists
            if not ("from" in data and "to" in data) and not "date" in data:
                return Response("Information incomplete",status=500)
            else:
                if "from" in data and "to" in data and "date" in data:
                    results = flights.find({"from": data["from"], "to": data["to"], "date": data["date"]}, {"businessTickets": 0, "businessPrice": 0, "economyTickets": 0, "economyPrice": 0})
                elif "from" in data and "to" in data:
                    results = flights.find({"from": data["from"], "to": data["to"]}, {"businessTickets": 0, "businessPrice": 0, "economyTickets": 0, "economyPrice": 0})
                elif "date" in data:
                    results = flights.find({"date": data["date"]}, {"businessTickets": 0, "businessPrice": 0, "economyTickets": 0, "economyPrice": 0}) 

                #put results in a list
                for result in results:
                    list.append({"_id":str(result["_id"]), "from":result["from"], "to":result["to"], "date":result["date"]})

                #return list in json format
                return jsonify(list)
        else:
            #if there is no data (body = {}), return all flights
            results = flights.find({}, {"businessTickets": 0, "businessPrice": 0, "economyTickets": 0, "economyPrice": 0})

            #put results in a list
            for result in results:
                    list.append({"_id":str(result["_id"]), "from":result["from"], "to":result["to"], "date":result["date"]})

            #return list in json format
            return jsonify(list)

    except Exception as e:
        return Response("Bad json content",status=500)





#endpoint to show flight details
@app.route("/showFlightDetails", methods=['POST'])
#authentication required for this endpoint
@token_required
def show_flight_details():
    #get token argument
    token = request.args.get("token")
    #decode token
    raw = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    #check if token belongs to an admin or a simple user
    if raw["role"] != "admin" and raw["role"] != "simpleUser":
        return Response("Access denied", status=403) 

    #Request JSON data
    data = None 

    try:

        #data has to include the _id (not the ObjectId - only the characters)
        data = json.loads(request.data)
        
        if not "_id" in data:
            return Response("Information incomplete",status=500)
        else:
            #find flight with that id
            flight = flights.find_one({"_id": ObjectId(data["_id"])})

            #find total number of tickets
            totalTickets = flight['economyTickets'] + flight['businessTickets']
            #find number of available tickets
            availableTickets = totalTickets - bookings.count_documents({"flightId": data["_id"]})
            #find available economy tickets
            availableEconomyTickets = flight["economyTickets"] - bookings.count_documents({"flightId": data["_id"], "ticketType":"economy"})
            #find available business tickets
            availableBusinessTickets = flight["businessTickets"] - bookings.count_documents({"flightId": data["_id"], "ticketType":"business"})

            #find bookings for this flight
            results = bookings.find({"flightId": data["_id"]})
            list = []
            #put results in a list
            for result in results:
                list.append({"name":str(result["name"]), "surname":result["surname"], "ticketType":result["ticketType"]})

            #transform list in json format
            booking_list = json.dumps(list)

            
            if raw["role"] == "admin": #in case this is an admin
                return jsonify({"from": flight["from"], "to": flight["to"], "totalTickets": totalTickets, "economyTickets": flight['economyTickets'], "businessTickets": flight['businessTickets'], "economyPrice": flight['economyPrice'], "businessPrice": flight['businessPrice'], "availableTickets": availableTickets, "availableEconomyTickets": availableEconomyTickets, "availableBusinessTickets": availableBusinessTickets, "bookings": booking_list})
            elif raw["role"] == "simpleUser": #in case this is a simple user
                return jsonify({"date": flight["date"], "from": flight["from"], "to": flight["to"], "economyTickets": flight['economyTickets'], "businessTickets": flight['businessTickets'], "economyPrice": flight['economyPrice'], "businessPrice": flight['businessPrice']})

    except Exception as e:
        return Response("Bad json content",status=500)





#Run Flask App
if __name__ == "__main__":
    app.run(debug=True. host="0.0.0.0")
