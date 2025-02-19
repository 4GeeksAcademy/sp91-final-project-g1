"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Teams, Matches, Coaches, Players


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return response_body, 200

# CRUD de Teams
@api.route('/teams', methods=['GET'])
def teams():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Teams)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of teams"
        response_body['results'] = result
        return response_body, 200


# CRUD de Matches
@api.route('/fixtures', methods=['GET', 'POST'])
def matches():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Matches)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of matches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_match = Matches(
            date = data.get('date'),
            home_team_id = data.get('home_team_id'),
            away_team_id = data.get('away_team_id'),
            home_goals = data.get('home_goals'),
            away_goals = data.get('away_goals'),
            is_home_winner = data.get('is_home_winner'))
        db.session.add(new_match)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_match.serialize()
        return response_body, 201
    

# CRUD de Coaches
@api.route('/coachs', methods=['GET', 'POST'])
def coaches():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Coaches)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of coaches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_coach = Coaches(
            name = data.get('name'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            nationality = data.get('nationality'),
            photo = data.get('photo'),
            team_id = data.get('team_id'))
        db.session.add(new_coach)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_coach.serialize()
        return response_body, 201

@api.route('/coachs/<int:id>', methods=['GET'])
def coach(id):
    response_body = {}
    coach = db.session.get(Coaches, id)
    if not coach:
        response_body['message'] = "Coach not found"
        return response_body, 404


# CRUD de Players
@api.route('/players/profiles', methods=['GET', 'POST'])
def players():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Players)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of players"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_player = Players(
            name = data.get('name'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            number = data.get('number'),
            nationality = data.get('nationality'),
            position = data.get('position'),
            photo = data.get('photo'),
            team_id = data.get('team_id'))
        db.session.add(new_player)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_player.serialize()
        return response_body, 201