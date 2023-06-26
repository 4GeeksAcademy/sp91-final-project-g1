"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import get_jwt_identity

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/configuration/<int:user_id>', methods=['GET'])
def configuration(user_id):
    user=User.query.filter_by(id = user_id).first()
    response_body = {
        "data": user.serialize()
    }

    return jsonify(response_body), 200


@api.route('/configuration', methods=['PUT'])
@get_jwt_identity()
def update_configuration():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    document_type = data.get('document_type')
    document_number = data.get('document_number')
    address = data.get('address')
    phone = data.get('phone')

    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if document_type:
        user.document_type = document_type
    if document_number:
        user.document_number = document_number
    if address:
        user.address = address
    if phone:
        user.phone = phone

    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating user"}), 500