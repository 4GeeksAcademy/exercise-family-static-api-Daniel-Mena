"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def member(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)
    if member == None:
         return jsonify({"message": "There is no user with the id " + str(id)}), 404
    else:
        response_body = member
        return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(id)
    if member == None:
        return jsonify({"message": "There is no user with the id " + str(id)}), 404
    else:
        response_body = member
        return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_new_member():
    request_body = request.json

    new_member = {
        "id": jackson_family._generateId(),
        "first_name": request_body["first_name"],
        "last_name": jackson_family.last_name,
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }

    member = jackson_family.add_member(new_member)

    response_body = str(new_member["first_name"]) + " " + str(new_member["last_name"])

    return jsonify({"message": "Member " + response_body +  " added successfully"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
