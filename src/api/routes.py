"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, FantasyLeagues, FantasyStandings, FantasyLeagueTeams,Teams, Matches, Coaches, Players


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
@api.route('/fantasy-leagues', methods=['GET', 'POST'])
def fantasy_leagues():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyLeagues)).scalars()
        result = [ row.serialize() for row in rows]
        response_body['message'] = f'List of fantasy league'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_league = FantasyLeagues(name=data.get('name'),
                                    photo=data.get('photo'))     
        db.session.add(new_league)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_league.serialize()
        return response_body, 201


@api.route('/fantasy-leagues/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_league(id):
    response_body = {}
    row = db.session.get(FantasyLeagues, id)
    if not row:
        response_body['message'] = f'El jugador de fantasy con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row.name = data['name']
        row.photo = data['photo']
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    

@api.route('/fantatsy-league-teams', methods=['GET', 'POST'])
def fantasy_league_teams():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyLeagueTeams)).scalars()
        result = [ row.serialize() for row in rows]
        response_body['message'] = f'List of fantasy league teams'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_league_team = FantasyLeagueTeams(fantasy_team_id=data.get('fantasy_team_id'),
                                             fantasy_league_id=data.get('fantasy_league_id'))     
        db.session.add(new_league_team)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_league_team.serialize()
        return response_body, 201


@api.route('/fantasy-league-teams/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_league_team(id):
    response_body = {}
    rows = db.session.get(FantasyLeagueTeams, id)
    if not rows:
        response_body['message'] = f'La liga de fantasy con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['results'] = rows.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        rows.fantasy_team_id = data['fantasy_team_id']
        rows.fantasy_league_id = data['fantasy_league_id']
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = rows.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(rows)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200


@api.route('/fantatsy-standings', methods=['GET', 'POST'])
def fantasy_standings():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyStandings)).scalars()
        result = [ row.serialize() for row in rows]
        response_body['message'] = f'List of fantasy standings'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_standing = FantasyStandings(fantasy_team_id=data.get('fantasy_team_id'))     
        db.session.add(new_standing)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_standing.serialize()
        return response_body, 201


@api.route('/fantasy-standings/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_standing(id):
    response_body = {}
    rows = db.session.get(FantasyStandings, id)
    if not rows:
        response_body['message'] = f'El fantasy standings con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['results'] = rows.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        rows.fantasy_team_id = data['fantasy_team_id']
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = rows.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(rows)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200


@api.route('/users', methods=['GET'])
def users():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Users)).scalars()
        result = [ row.serialize() for row in rows]
        response_body['message'] = 'List de users'
        response_body['results'] = result
        return response_body, 200
    

@api.route('/users/<int:id>', methods=['GET', 'PUT'])
def user(id):
    response_body = {}
    row = db.session.get(Users, id)
    if not row:
        response_body['message'] = f'El comentario con el id: {id} no existe en nuestro registros'
        return response_body, 400
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row.username = data['username']
        row.email = data['email']
        row.password = data['password']
        row.phone_number = data['phone_number']
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    
