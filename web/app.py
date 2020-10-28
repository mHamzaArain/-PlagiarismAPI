"""
Service API
------------

* Registration of a user with 6 tokens initially.
* Detect similarity between text1 and text2 then return ratio database for 1 token and .
* Admin can refill tokens.

@author Hamza Arain
@version 0.0.1v
@date 28 October 2020

"""


# import modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

import bcrypt



# ###########################################################
# #######################  Tool Class ######################
# ###########################################################    
class Tool():
    def JSONOutputMessage(statusCode, output="", ratio=0):
        """Return status code 200 & output"""
        if ratio != 0:
            retMap = {
                'Message': output,
                'Status Code': statusCode,
                'ratio': ratio
            }
            return jsonify(retMap)
        retMap = {
                'Message': output,
                'Status Code': statusCode
            }
        return jsonify(retMap)


    def verifyPw(username, password):
        """varify password from database"""
        hashed_pw = users.find({
            "Username":username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False

    def countTokens(username):
        tokens = users.find({
            "Username":username
        })[0]["Tokens"]
        return tokens


    def UserExist(username):
        if users.find({"Username":username}).count() == 0:
            return False
        else:
            return True

    def nlp(text1, text2):
        #Calculate edit distance between text1, text2
        import spacy
        nlp = spacy.load('en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)
        return ratio



# ###########################################################
# #######################  API Classes ######################
# ###########################################################    

class Register(Resource):
    def post(self):
        """Register new user with 6 tokens"""
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"
        
        if Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username")

        # hashing + salt
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":6
        })

        return Tool.JSONOutputMessage(statusCode=200, output="You successfully signed up for the API")


class Detect(Resource):
    def post(self):
        """Detect Plagiarism for one token"""
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username")
        #Step 3 verify the username pw match
        correct_pw = Tool.verifyPw(username, password)

        if not correct_pw:
            return Tool.JSONOutputMessage(statusCode=302, output="Invalid Password")
        # Step 4 Verify user has enough tokens
        num_tokens = Tool.countTokens(username)
        
        if num_tokens <= 0:
            return Tool.JSONOutputMessage(statusCode=303, output="You are out of tokens, please refill!")

        # Take away 1 token from user
        current_tokens = Tool.countTokens(username)
        users.update({
            "Username":username
        }, {
            "$set":{
                "Tokens":current_tokens-1
                }
        })

        # return jsonify(retJson)
        return Tool.JSONOutputMessage(statusCode=200, output="Similarity score calculated successfully", ratio=Tool.nlp(text1=text1, text2=text2))

class Refill(Resource):
    """Refill tokens by admin to user"""
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]

        if not Tool.UserExist(username):
            return Tool.JSONOutputMessage(statusCode=301, output="Invalid Username")


        correct_pw = "abc123"
        if not password == correct_pw:
            return Tool.JSONOutputMessage(statusCode=304, output="Invalid Admin Password")

        #MAKE THE USER PAY!
        users.update({
            "Username":username
        }, {
            "$set":{
                "Tokens":refill_amount
                }
        })
        return Tool.JSONOutputMessage(statusCode=200, output="Refilled successfully")

# ###########################################################
# ##################### Run Application #####################
# ###########################################################


# Database connection
# # "db" is same as written in web Dockerfile
# # "27017" is default port for MongoDB 
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

# App & API creation
app = Flask(__name__)
api = Api(app)

# API paths
api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')


if __name__=="__main__":
    app.run(host='0.0.0.0')
