"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import requests
import dotenv
import os
import bcrypt
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Teams, Matches, Coaches, Players, FantasyCoaches, FantasyTeams, FantasyPlayers, Users, FantasyLeagues, FantasyStandings, FantasyLeagueTeams
from datetime import datetime
import numpy as np
import urllib.request
import base64
import cv2


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API
dotenv.load_dotenv()


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return response_body, 200


def populate_fixtures(headers, params):
    url = f'https://{os.getenv("API_URL")}/fixtures'
    result = requests.get(url, params=params, headers=headers)
    rows = result.json().get('response')
    for row in rows:
        fixture = row.get('fixture')
        teams = row.get('teams')
        goals = row.get('goals')
        home_goals = goals.get('home')
        away_goals = goals.get('away')
        new_fixture = Matches(
            uid = fixture.get('id'),
            date = fixture.get('date'),
            home_team_id = teams.get('home').get('id'),
            away_team_id = teams.get('away').get('id'),
            home_goals = home_goals,
            away_goals = away_goals,
            is_home_winner = home_goals > away_goals)
        db.session.add(new_fixture)
    db.session.commit()
    return


def populate_teams(params, headers):
    url = f'https://{os.getenv("API_URL")}/teams'
    result = requests.get(url, params=params, headers=headers)
    rows = result.json().get('response')
    teams = []
    for row in rows:
        team = row.get('team')
        new_team = Teams(
            uid = team.get('id'),
            name = team.get('name'),
            logo = team.get('logo'))
        db.session.add(new_team)
        teams.append(new_team)
    db.session.commit()
    return teams


def populate_coach(params, headers):
    url = f'https://{os.getenv("API_URL")}/coachs'
    result = requests.get(url, params=params, headers=headers)
    rows = result.json().get('response')
    fecha_limite = datetime(2024, 5, 26)
    print(result.json())
    for coach in rows:
        coach_career = coach.get('career')
        for coach_team in coach_career:
            start_date = datetime.strptime(coach_team.get('start'), '%Y-%m-%d')
            end_date = datetime.strptime(coach_team.get('end'), '%Y-%m-%d') if coach_team.get('end') is not None else datetime(9999, 1, 1)
            if (end_date is None and start_date < fecha_limite) or (end_date is not None and end_date > fecha_limite):
                if db.session.execute(db.select(Coaches).where(Coaches.uid == coach.get("id"))).scalar() is not None:
                    print(f'Entrenador repetido: {coach.get("id")} = {coach.get("firstname")} {coach.get("lastname")}')
                    return
                new_coach = Coaches(
                    uid = coach.get('id'),
                    name = coach.get('name'),
                    first_name = coach.get('firstname'),
                    last_name = coach.get('lastname'),
                    nationality = coach.get('nationality'),
                    photo = coach.get('photo'),
                    team_id = coach.get('team').get('id'))
                db.session.add(new_coach)
                return  # Evitamos que hayan dos entrenadores por equipo o que el mismo entrenador salga dos veces


def populate_players(initial_params, headers):
    params = initial_params
    url = f'https://{os.getenv("API_URL")}/players'

    while True:
        result = requests.get(url, params=params, headers=headers)
        data = result.json()
        current = data.get("paging").get("current")
        total = data.get("paging").get("total")
        rows = data.get("response")
        print(f'page {current} of {total} - team: {params.get("team")}')
        for row in rows:
            player_row = row.get("player")
            stats = row.get("statistics")[0]
            if db.session.execute(db.select(Players).where(Players.uid == player_row.get("id"))).scalar() is not None:
                print(f'Jugador repetido: {player_row.get("id")} = {player_row.get("firstname")} {player_row.get("lastname")} - team: {stats.get("team").get("id")}')
                continue
            player = Players(
                uid=player_row.get("id"),
                name=player_row.get("name"),
                first_name=player_row.get("firstname") if player_row.get("firstname") is not None else "",
                number=0,  # TODO: Quitar esta variable
                last_name=player_row.get("lastname") if player_row.get("lastname") is not None else "",
                nationality=player_row.get("nationality"),
                position=stats.get("games").get("position"),
                photo=player_row.get("photo"),
                team_id=params.get("team")
            )
            db.session.add(player)
        if current == total:
            print("----------------------------------------")
            break
        params["page"] = current + 1
    db.session.commit()
    return


@api.route('/populate-db-1', methods=['GET'])
def populate_db():
    params = { "league": 140, "season": 2023}
    headers = { "x-rapidapi-host": os.getenv("API_URL"),
                "x-rapidapi-key": os.getenv("API_KEY") }
    populate_teams(params=params, headers=headers)
    populate_fixtures(params=params, headers=headers)
    db.session.commit()
    print("Base de datos actualizada correctamente")
    return {}, 200


"""
    Ejecutar esta función después de la de arriba, los ids del equipo se pasarán por parámetro. 
    Hay que hacer varias llamadas debido a la restriccion de 10 peticiones por minuto

    @params peticion 1: ?team_ids=529,530,531
    @params peticion 2: ?team_ids=532,533,534
    @params peticion 3: ?team_ids=536,538,541
    @params peticion 4: ?team_ids=542,543,546
    @params peticion 5: ?team_ids=547,548,715
    @params peticion 6: ?team_ids=723,724,727
    @params peticion 7: ?team_ids=728,798
"""
@api.route('/populate-players', methods=['GET'])
def populate_db_players():
    ids = request.args.get("team_ids").split(",")
    for id in ids:
        params = { "league": 140, "season": 2023, "team": id }
        headers = { "x-rapidapi-host": os.getenv("API_URL"),
                "x-rapidapi-key": os.getenv("API_KEY") }
        populate_players(initial_params=params, headers=headers)
    db.session.commit()
    print("Jugadores actualizados")
    return {}, 200


"""
    Ejecutar esta función después de /populate-db-1, los ids del equipo se pasarán por parámetro. 
    Hay que hacer varias llamadas debido a la restriccion de 10 peticiones por minuto

    @params peticion 1: ?team_ids=529,530,531,532,533,534,536,538,541,542
    @params peticion 2: ?team_ids=543,546,547,548,715,723,724,727,728,798
"""
@api.route('/populate-coaches', methods=['GET'])
def populate_db_coaches():
    ids = request.args.get("team_ids").split(",")
    headers = { "x-rapidapi-host": os.getenv("API_URL"),
                "x-rapidapi-key": os.getenv("API_KEY") }
    for id in ids:
        params = { "team": id }
        populate_coach(params=params, headers=headers)
    db.session.commit()
    print("Entrenadores actualizados")
    return {}, 200


# CRUD de Teams
@api.route('/teams', methods=['GET', 'POST'])
def teams():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Teams)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of teams"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_team = Teams(
            name = data.get('name'),
            logo = data.get('logo'))
        db.session.add(new_team)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_team.serialize()
        return response_body, 201


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

"""
@api.route('/players-market', methods=['GET'])
def players_market():
    limit = request.args.get("limit")
    response_body = {}
    players_rows = db.session.execute(db.select(Players).limit(limit)).scalars()

    def serialize(row):
        serialized_row = row.serialize()
        team_row = db.session.execute(db.select(Teams).where(Teams.uid == row.team_id)).scalar()
        if team_row == None:
            return serialized_row
        team = team_row.serialize()
        serialized_row["team"] = team
        return serialized_row
    
    result = [serialize(row) for row in players_rows]
    
    response_body['message'] = "List of players"
    response_body['results'] = result
    return response_body, 200
"""

# CRUD de Players
@api.route('/players', methods=['GET', 'POST'])
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


def generate_password_hash(password):
    bytes = str(password).encode('utf-8')
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode("utf-8")

@api.route('/users', methods=['GET', 'POST'])
def users():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(Users)).scalars()
        result = [ row.serialize() for row in rows]
        response_body['message'] = 'List de users'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        username = data.get('username', None),
        email = data.get('email', None),
        password = data.get('password', None)
        phone_number = data.get('phone_number', None)
        hash_password = generate_password_hash(password)
        new_user = Users(username = username, email = email, password = hash_password, phone_number = phone_number, is_active = True)
        db.session.add(new_user)
        db.session.commit()
        response_body['message'] = 'Usuario creado correctamente'
        response_body['results'] = new_user.serialize()
        return response_body, 201


@api.route('/login', methods=['POST'])
def login():
    response_body = {}
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user_row = db.session.execute(db.select(Users).where(Users.email == email, Users.is_active == True)).scalar()
    if user_row == None:
        response_body['message'] = 'Usuario no existente'
        return response_body, 404
    password_bytes = password.encode('utf-8')
    user_password_bytes = user_row.password.encode('utf-8')
    if bcrypt.checkpw(password=password_bytes, hashed_password=user_password_bytes) == True:
        user_data = user_row.serialize()
        access_token = create_access_token(identity=str(user_data["id"]), additional_claims={'user_id': user_data["id"], 'is_active': user_data['is_active']})
        response_body['message'] = 'Usuario correcto'
        response_body['access_token'] = access_token
        response_body['results'] = user_data
        return response_body, 201
    else:
        response_body['message'] = 'Datos incorrectos'
        return response_body, 400


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


# CRUD de Fantasy Coach
@api.route('/fantasy-coaches', methods=['GET', 'POST'])
def fantasy_coaches():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyCoaches)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of fantasy coaches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_coach = FantasyCoaches(
            coach_id = data.get('coach_id'),
            fantasy_team_id = data.get('fantasy_team_id'),
            points = 0,
            market_value = 0,
            clause_value = 0)
        db.session.add(new_coach)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_coach.serialize()
        return response_body, 201


@api.route('/fantasy-coaches/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_coach(id):
    response_body = {}
    fantasy_coach = db.session.get(FantasyCoaches, id)
    if not fantasy_coach:
        response_body['message'] = "Fantasy coach not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_coach.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_coach.coach_id = data.get("coach_id", fantasy_coach.coach_id)
        fantasy_coach.fantasy_team_id = data.get("fantasy_team_id", fantasy_coach.fantasy_team_id)
        fantasy_coach.points = data.get("points", fantasy_coach.points)
        fantasy_coach.market_value = data.get("market_value", fantasy_coach.market_value)
        fantasy_coach.clause_value = data.get("clause_value", fantasy_coach.clause_value)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_coach.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_coach)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        return response_body, 200


# CRUD de Fantasy Team
@api.route('/fantasy-teams', methods=['GET', 'POST'])
def fantasy_teams():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyTeams)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of fantasy teams"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_team = FantasyTeams(
            user_id = data.get('user_id'),
            name = data.get('name'),
            logo = data.get('logo'),
            formation = "4-3-3",
            points = 0)
        db.session.add(new_team)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_team.serialize()
        return response_body, 201


@api.route('/fantasy-teams/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_team(id):
    response_body = {}
    fantasy_team = db.session.get(FantasyTeams, id)
    if not fantasy_team:
        response_body['message'] = "Fantasy team not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_team.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_team.user_id = data.get("user_id", fantasy_team.user_id)
        fantasy_team.name = data.get("name", fantasy_team.name)
        fantasy_team.logo = data.get("logo", fantasy_team.logo)
        fantasy_team.formation = data.get("formation", fantasy_team.formation)
        fantasy_team.points = data.get("points", fantasy_team.points)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_team.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_team)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        return response_body, 200
 

# CRUD de Fantasy Player
@api.route('/fantasy-players', methods=['GET', 'POST'])
def fantasy_players():
    response_body = {}
    if request.method == 'GET':
        rows = db.session.execute(db.select(FantasyPlayers)).scalars()
        result = [row.serialize() for row in rows]
        response_body['message'] = "List of fantasy players"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_player = FantasyPlayers(
            player_id = data.get('player_id'),
            fantasy_team_id = data.get('fantasy_team_id'),
            position = 0,
            points = 0,
            market_value = 0,
            clause_value = 0,
            is_scoutable = True)
        db.session.add(new_player)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_player.serialize()
        return response_body, 201


@api.route('/fantasy-players/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_player(id):
    response_body = {}
    fantasy_player = db.session.get(FantasyPlayers, id)
    if not fantasy_player:
        response_body['message'] = "Fantasy player not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_player.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_player.player_id = data.get("player_id", fantasy_player.player_id)
        fantasy_player.fantasy_team_id = data.get("fantasy_team_id", fantasy_player.fantasy_team_id)
        fantasy_player.position = data.get("position", fantasy_player.position)
        fantasy_player.points = data.get("points", fantasy_player.points)
        fantasy_player.market_value = data.get("market_value", fantasy_player.market_value)
        fantasy_player.clause_value = data.get("clause_value", fantasy_player.clause_value)
        fantasy_player.is_scoutable = data.get("is_scoutable", fantasy_player.is_scoutable)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_player.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_player)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        return response_body, 200


@api.route('/remove-bg', methods=['POST'])
def remove_bg():
    response_body = {}
    data = request.json
    req = urllib.request.urlopen(data.get("image_url"))
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    Z = img.reshape((-1, 3))
    Z = np.float32(Z)

    K = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    dominant_colors = centers[np.argmax(np.bincount(labels.flatten()))]

    dominant_hsv = cv2.cvtColor(np.uint8([[dominant_colors]]), cv2.COLOR_BGR2HSV)[0][0]

    lower_white = np.array([0, 0, dominant_hsv[2] - 5], dtype=np.uint8)
    upper_white = np.array([255, 5, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < 2000:
            cv2.drawContours(mask, [cnt], -1, 0, -1)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[:, :, 3] = 255 - mask

    _, buffer = cv2.imencode(".png", img)
    response_body['results'] = base64.b64encode(buffer).decode("utf-8")
    return response_body, 200


#CRUD Actualizar Datos Usuario
@api.route('/update-user', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    data = request.json
    print(user_id)
    user = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.phone_number = data.get("phone_number", user.phone_number)

    db.session.commit()

    return jsonify({
        "message": "Datos actualizados correctamente",
        "results": user.serialize()
    }), 200


# CRUD Eliminar Usuario
@api.route('/delete-user', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    
    user = db.session.get(Users, user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Cuenta eliminada correctamente"}), 200


# CRUD Cambiar Contraseña
@api.route('/reset-password', methods=['PUT'])
@jwt_required()
def reset_password():
    user_id = get_jwt_identity()
    data = request.json
    print(data)
    new_password = data.get("password")

    user = db.session.get(Users, user_id) 
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    print(user)
    
    user.password = generate_password_hash(new_password)

    db.session.commit()
    print("Se ha guardado en base de datos")

    return jsonify({
        "message": "Contraseña actualizada correctamente"
    }), 200

