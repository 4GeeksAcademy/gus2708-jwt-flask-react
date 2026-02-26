"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, BlockedToken
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


api = Blueprint('api', __name__)
bcrypt = Bcrypt()

# Allow CORS requests to this API
CORS(api)

# registro de usuario


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

# login de usuario


@api.route('/login', methods=['POST'])
def login_creating_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

# si el usuario no existe o la contraseña es incorrecta, devolvemos un error 401
    if user is None:
        return jsonify({"error": "user does not exist"}), 401

# comprobamos la contraseña usando bcrypt, si es incorrecta devolvemos un error 401
    if bcrypt.check_password_hash(user.password, password) is False:
        return jsonify({"error": "The passwors is incorrect"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"msg": f"user {email} was succesfully loged", "access_token": access_token}), 200

# ruta oritegida para ver info de perfil, solo se puede acceder con un token valido


@api.route('/profile',  methods=['GET'])
@jwt_required()
def get_profile_information():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # si el usuario no existe, devolvemos un error 401
    if user is None:
        return jsonify({"error": "user does not exist"}), 401
    return jsonify(user.serialize()), 200


@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"] 
    blocked_token = BlockedToken(jti=jti)
    db.session.add(blocked_token)
    db.session.commit()
    return jsonify({"msg": "User logged out successfully"}), 200