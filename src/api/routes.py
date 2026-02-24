"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


api = Blueprint('api', __name__)
bcrypt = Bcrypt()

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def register_user():
    # obtenemos los parametros del request
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # comprobamos si el usuario con ese correo ya existe
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User already exists"})

    new_user = User(email=email, password=bcrypt.generate_password_hash(
        password).decode('utf-8'), is_active=True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User with email " + email + " created"}), 201

@api.route('/login', methods=['POST'])
def login_creating_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "user does not exist"}), 401

    if bcrypt.check_password_hash(user.password, password) is False:
        return jsonify({"error": "The passwors is incorrect"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({"msg": f"user {email} was succesfully loged", "access_token": access_token}), 200

@api.route('/profile',  methods=['GET'])
@jwt_required()
def get_profile_information():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "user does not exist"}), 401
    return jsonify(user.serialize()), 200
