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
from api.models import db, Teams, Matches, Coaches, Players, FantasyCoaches, FantasyTeams, FantasyPlayers, Users, FantasyLeagues, FantasyStandings, FantasyLeagueTeams, Standings
from datetime import datetime
import numpy as np
import urllib.request
import base64
import cv2
from api.functions import *


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


"""
    CRUD /users

    GET /: Obtiene todos los usuarios
    POST /: Crea un usuario
        Ejemplo de body: {"username": "Test",
                          "email": "test@email.com",
                          "password": "1234", # Se encripta desde el backend
                          "phone_number": "123456789"}
    GET /<id>: Obtiene los datos de un usuario mediante su ID
    PUT /<id>: Actualiza los datos de un usuario
        Ejemplo de body: {"username": "Other",
                          "email": "other@email.com",
                          "phone_number": "987654321"}
    DELETE /<id>: Elimina un usuario (soft delete)
    PUT /reset-password: Restablece la contraseña a una ofrecida por el usuario
        Ejemplo de body: {"password": "5678"}

    GET /<id>/fantasy-teams: Devuelve el equipo de un usuario
    POST /<id>/join-league/<league_id>': Añade al usuario a una liga y le crea un equipo
        Ejemplo de body: {"id": 1,
                          "league_id": 1}
"""
@api.route('/users', methods=['GET', 'POST'])
def users():
    response_body = {}
    if request.method == 'GET':
        result = get_users()
        response_body['message'] = 'List de users'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        user_existing = get_user_by_email(email=data.get('email'))
        if user_existing is not None: 
            response_body["message"] = "Usuario ya existente"
            return response_body, 403
        username = data.get('username', None),
        email = data.get('email', None),
        password = data.get('password', None)
        phone_number = data.get('phone_number', None)
        new_user = add_user(username = username, 
                            email = email, 
                            password = password, 
                            phone_number = phone_number)
        response_body['message'] = 'Usuario creado correctamente'
        response_body['results'] = new_user.serialize()
        return response_body, 201


@api.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user(id):
    response_body = {}
    row = get_user_by_id(id=id)
    if not row:
        response_body['message'] = f'El usuario con el id: {id} no existe en nuestro registros'
        return response_body, 400
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        user_id = get_jwt_identity()
        data = request.json
        user = get_user_by_id(id=user_id)
        user = update_user(user=user, 
                           username=data.get('username'), 
                           email=data.get('email'), 
                           phone_number=data.get('phone_number'))
        response_body["message"] = "Datos actualizados correctamente",
        response_body["results"] = user.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        user_id = get_jwt_identity()
        user = get_user_by_id(id=user_id)

        if not user:
            response_body["message"] = "Usuario no encontrado"
            return response_body, 404

        delete_user(user=user)

        response_body["message"] = "Cuenta deshabilitada correctamente"
        return response_body, 200


@api.route('users/reset-password', methods=['PUT'])
@jwt_required()
def reset_password():
    response_body = {}
    user_id = get_jwt_identity()
    data = request.json
    new_password = data.get("password")

    user = get_user_by_id(id=user_id)
    if not user:
        response_body["message"] = "Usuario no encontrado"
        return response_body, 404
    
    user.password = generate_password_hash(new_password)
    db.session.commit()

    response_body["message"] = "Contraseña actualizada correctamente"
    return response_body, 200


@api.route('/users/<int:id>/fantasy-teams', methods=['GET'])
def fantasy_team_by_user(id):
    response_body = {}
    row = get_fantasy_team_by_user_id(id)
    if row is None:
        response_body['message'] = "Fantasy team not found"
        return response_body, 404

    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = row.serialize()
        return response_body, 200
    return row.serialize()


@api.route('/users/<int:id>/join-league/<int:league_id>', methods=['POST'])
def join_league(id, league_id):
    response_body = {}
    new_team_of_league = add_user_to_league(id, league_id)

    response_body['message'] = f'Respuesta desde {request.method}'
    response_body['results'] = new_team_of_league.serialize()
    return response_body, 201


@api.route('/login', methods=['POST'])
def login():
    response_body = {}
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user_row = get_active_user_by_email(email=email)
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


"""
    CRUD /teams
    
    GET /: Obtiene todos los equipos
    POST /: Crea un equipo
        Ejemplo de body: {"id": 1,
                          "name": "Test FC",
                          "logo" "https://media.api-sports.io/football/teams/1.png"}
"""
@api.route('/teams', methods=['GET', 'POST'])
def teams():
    response_body = {}
    if request.method == 'GET':
        result = get_teams()
        response_body['message'] = "List of teams"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_team = add_team(
            uid=data.get("id"),
            name=data.get('name'), 
            logo=data.get('logo')
        )
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_team
        return response_body, 201


"""
    CRUD /matches
    
    GET /: Obtiene todos los partidos
    POST /: Crea un partido
        Ejemplo de body: {"data": 01/01/1970,
                          "home_team_id": 1,
                          "away_team_id": 2,
                          "home_goals": 1,
                          "away_goals": 0,
                          "is_home_winner": True}
"""
@api.route('/matches', methods=['GET', 'POST'])
def matches():
    response_body = {}
    if request.method == 'GET':
        result = get_matches()
        response_body['message'] = "List of matches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_match = add_match(
            date = data.get('date'),
            home_team_id = data.get('home_team_id'),
            away_team_id = data.get('away_team_id'),
            home_goals = data.get('home_goals'),
            away_goals = data.get('away_goals'),
            is_home_winner = data.get('is_home_winner')
        )
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_match
        return response_body, 201


@api.route('/standings', methods=['GET', 'POST'])
def standings():
    response_body = {}
    today = datetime.now()
    league_day = datetime(today.year - 1, today.month, today.day)
    if request.method == 'GET':
        teams_data = get_standings()
        response_body['message'] = f'Partidos hasta {league_day}'
        response_body['results'] = sorted(teams_data, key=lambda d: d['points'], reverse=True)
        return response_body, 200
    if request.method == 'POST':
        teams_data = get_standings()
        teams_data = initialize_standings(create_new=len(teams_data) == 0)
        teams_data = calculate_standings(league_day)
        data = []
        for team_data in teams_data:
            standing = update_standing(
                team_id = team_data['team_id'],
                points = team_data['points'],
                games_won = team_data['games_won'],
                games_draw = team_data['games_draw'],
                games_lost = team_data['games_lost'],
                goals_for = team_data['goals_for'],
                goals_against = team_data['goals_against'],
                form = team_data['form'])
            data.append(standing)
        standings_data = get_standings()
        response_body['message'] = 'Standings inicializados correctamente'
        response_body['results'] = sorted(standings_data, key=lambda d: d['points'], reverse=True)
        return response_body, 201


"""
    CRUD /coaches
    
    GET /: Obtiene todos los entrenadores
    POST /: Crea un entrenador
        Ejemplo de body: {"id": 1,
                          "name": "T. Coach",
                          "first_name": "Test",
                          "last_name": "Coach",
                          "nationality": "Spain",
                          "photo": "https://media.api-sports.io/football/coachs/1.png",
                          "team_id": 1}
    GET /<id>: Obtiene todos los datos de un entrenador según su id
"""
@api.route('/coaches', methods=['GET', 'POST'])
def coaches():
    response_body = {}
    if request.method == 'GET':
        result = get_coaches()
        response_body['message'] = "List of coaches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_coach = add_coach(
            uid = data.get("id"),
            name = data.get('name'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            nationality = data.get('nationality'),
            photo = data.get('photo'),
            team_id = data.get('team_id'))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_coach
        return response_body, 201


@api.route('/coaches/<int:id>', methods=['GET'])
def coach(id):
    response_body = {}
    coach = get_coach_by_id(id=id)
    if not coach:
        response_body['message'] = "Coach not found"
        return response_body, 404
    return coach.serialize()


"""
    CRUD /players
    
    GET /: Obtiene todos los jugadores
    POST /: Crea un jugador
        Ejemplo de body: {"id": 1,
                          "name": "T. Coach",
                          "first_name": "Test",
                          "last_name": "Coach",
                          "number": 1,
                          "nationality": "Spain",
                          "position": "Goalkeeper",
                          "photo": "https://media.api-sports.io/football/players/1.png",
                          "team_id": 1}
"""
@api.route('/players', methods=['GET', 'POST'])
def players():
    response_body = {}
    if request.method == 'GET':
        result = get_players()
        response_body['message'] = "List of players"
        response_body['results'] = result
        return response_body, 200

    if request.method == 'POST':
        data = request.json
        new_player = add_player(
            name = data.get('name'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            number = data.get('number'),
            nationality = data.get('nationality'),
            position = data.get('position'),
            photo = data.get('photo'),
            team_id = data.get('team_id'))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_player.serialize()
        return response_body, 201


@api.route('/players-market', methods=['GET'])
def players_market():
    limit = request.args.get("limit", "15")
    page = request.args.get("page", "0")
    response_body = {}
    result = get_players_market(page=page, limit=limit)
    total_players = get_players()
    
    response_body['message'] = "List of players"
    response_body['results'] = result
    response_body['count'] = int(page)*int(limit) + len(result)
    response_body['total'] = len(total_players)
    return response_body, 200


"""
    CRUD /fantasy-leagues
    
    GET /: Obtiene todos los jugadores que están en una liga fantasy
    POST /: Crea una liga fantasy
        Ejemplo de body: {"name": "Test Liga",
                          "photo": "https://media.api-sports.io/football/leagues/1.png"}
    GET /<id>: Obtiene los datos de una liga fantasy mediante su ID
    PUT /<id>: Actualiza los datos de una liga
        Ejemplo de body: {"name": "Other Liga",
                          "photo": "https://media.api-sports.io/football/leagues/2.png"}
    DELETE /<id>: Elimina una liga fantasy (hard delete)
"""
@api.route('/fantasy-leagues', methods=['GET', 'POST'])
def fantasy_leagues():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_leagues()
        response_body['message'] = f'List of fantasy league'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_league = add_fantasy_league(name=data.get('name'),
                                    photo=data.get('photo'))     
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_league.serialize()
        return response_body, 201


@api.route('/fantasy-leagues/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_league(id):
    response_body = {}
    row = get_fantasy_league(id=id)
    if not row:
        response_body['message'] = f'La liga de fantasy con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row = update_fantasy_league(row, data.get('name'), data.get('photo'))
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    return row.serialize()


"""
    CRUD /fantasy-teams
    
    GET /: Obtiene todos los equipos que están en una liga fantasy
    POST /: Crea un equipo fantasy
        Ejemplo de body: {"user_id": 1
                          "name": "Other FC",
                          "logo": "https://media.api-sports.io/football/teams/1.png"}
    GET /<id>: Obtiene los datos de un equipo fantasy mediante su ID
    PUT /<id>: Actualiza los datos de un equipo
        Ejemplo de body: {"user_id": 1
                          "name": "Other FC",
                          "logo": "https://media.api-sports.io/football/teams/2.png",
                          "formation": "3-4-3",
                          "points": 0}
    DELETE /<id>: Elimina un equipo fantasy (hard delete)

    GET /<id>/fantasy-players: Obtiene todos los jugadores que están en un equipo fantasy
"""
@api.route('/fantasy-teams', methods=['GET', 'POST'])
def fantasy_teams():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_teams()
        response_body['message'] = "List of fantasy teams"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_team = add_fantasy_team(
            user_id = data.get('user_id'),
            name = data.get('name'),
            logo = data.get('logo'))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_team.serialize()
        return response_body, 201


@api.route('/fantasy-teams/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_team(id):
    response_body = {}
    fantasy_team = get_fantasy_team_by_id(id=id)
    if not fantasy_team:
        response_body['message'] = "Fantasy team not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_team.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_team = update_fantasy_team(
            fantasy_team=fantasy_team,
            name=data.get("name", fantasy_team.name),
            logo=data.get("logo", fantasy_team.logo),
            formation=data.get("formation", fantasy_team.formation),
            points=data.get("points", fantasy_team.points)
        )
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_team.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_team)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        return response_body, 200


@api.route('/fantasy-teams/<int:id>/fantasy-players', methods=['GET'])
def fantasy_players_by_team(id):
    response_body = {}
    fantasy_team = get_fantasy_team_by_id(id=id)
    if not fantasy_team:
        response_body['message'] = "Fantasy team not found"
        return response_body, 404
    data = get_fantasy_players_by_team(id=id)
    response_body['message'] = f'Respuesta desde {request.method}'
    response_body['results'] = data
    return response_body, 200


"""
    CRUD /fantasy-league-teams
    
    GET /: Obtiene todas las relaciones entre equipos fantasy y ligas fantasy
    POST /: Añade un equipo fantasy a una liga fantasy
        Ejemplo de body: {"fantasy_team_id": 1
                          "fantasy_league_id": 1}
    GET /<id> (en desuso): Obtiene la relación entre un equipo fantasy y una liga fantasy mediante su ID
    PUT /<id> (en desuso): Actualiza la relación entre un equipo fantasy y una liga fantasy
        Ejemplo de body: {"fantasy_team_id": 2
                          "fantasy_league_id": 2}
    DELETE /<id>: Elimina un equipo fantasy de una liga fantasy (hard delete)
"""
@api.route('/fantasy-league-teams', methods=['GET', 'POST'])
def fantasy_league_teams():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_league_teams()
        response_body['message'] = f'List of fantasy league teams'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_league_team = add_fantasy_league_team(fantasy_team_id=data.get('fantasy_team_id'),
                                             fantasy_league_id=data.get('fantasy_league_id'))
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_league_team.serialize()
        return response_body, 201


@api.route('/fantasy-league-teams/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_league_team(id):
    response_body = {}
    row = get_fantasy_league_team_by_id(id=id)
    if not row:
        response_body['message'] = f'La liga de fantasy con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row = update_fantasy_league_team(row, data.get('fantasy_team_id'), data.get('fantasy_league_id'))
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200


"""
    CRUD /fantasy-players
    
    GET /: Obtiene todos los jugadores fantasy
    POST /: Añade un equipo fantasy a una liga fantasy
        Ejemplo de body: {"player_id": 1,
                          "fantasy_team_id": 1,
                          "position": "Goalkeeper",
                          "clause_value": 123456789}
    GET /<id>: Obtiene un jugador fantasy mediante su ID
    PUT /<id>: Actualiza un jugador fantasy
        Ejemplo de body: {"fantasy_team_id": 2,
                          "position": "Defender",
                          "clause_value": 987654321}
    DELETE /<id>: Elimina un jugador fantasy (hard delete)

    GET /<id>/fantasy-teams: Obtiene un jugador fantasy con los datos del equipo fantasy al que pertenece
"""
@api.route('/fantasy-players', methods=['GET', 'POST'])
def fantasy_players():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_players()
        response_body['message'] = "List of fantasy players"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_player = add_fantasy_player(
            player_id = data.get('player_id'),
            fantasy_team_id = data.get('fantasy_team_id'),
            position = data.get('position'),
            clause_value = data.get('clause_value'))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_player.serialize()
        return response_body, 201


@api.route('/fantasy-players/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_player(id):
    response_body = {}
    fantasy_player = get_fantasy_player_by_id(id)
    if not fantasy_player:
        response_body['message'] = "Fantasy player not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_player.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_player = update_fantasy_player(fantasy_player=fantasy_player,
                                               fantasy_team_id=data.get('fantasy_team_id', fantasy_player.fantasy_team_id),
                                               points=data.get('points', fantasy_player.points),
                                               clause_value=data.get('clause_value', fantasy_player.clause_value),
                                               is_scoutable=data.get('is_scoutable', fantasy_player.is_scoutable))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_player.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_player)
        db.session.commit()
        response_body['message'] = f'Respuesta desde {request.method}'
        return response_body, 200


@api.route('/fantasy-players/<int:id>/fantasy-teams', methods=['GET'])
def fantasy_player_with_team_data(id):
    response_body = {}
    fantasy_player = get_fantasy_player_with_team_data(id)
    if fantasy_player is None:
        return response_body, 404
    response_body['results'] = fantasy_player
    return response_body, 200


"""
    CRUD /fantasy-standings
    
    GET /: Obtiene todos los standings de todas las ligas fantasy
    POST /: Añade un fantasy standing
        Ejemplo de body: {"fantasy_team_id": 1}
    GET /<id> (TODO: obtener mediante fantasy_team_id): Obtiene un fantasy standing mediante su ID
    PUT /<id> (TODO: calcular fantasy standing): Actualiza un jugador fantasy
        Ejemplo de body: {"fantasy_team_id": 2}
    DELETE /<id>: Elimina un jugador fantasy (hard delete)

    GET /<id>/fantasy-teams: Obtiene un jugador fantasy con los datos del equipo fantasy al que pertenece
"""
@api.route('/fantatsy-standings', methods=['GET', 'POST'])
def fantasy_standings():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_standings()
        response_body['message'] = f'List of fantasy standings'
        response_body['results'] = result
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        new_standing = add_fantasy_standing(fantasy_team_id=data.get('fantasy_team_id'))
        response_body['message'] = f'Respuesta desde el {request.method}'
        response_body['results'] = new_standing.serialize()
        return response_body, 201


@api.route('/fantasy-standings/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_standing(id):
    response_body = {}
    row = get_fantasy_standing(id=id)
    if not row:
        response_body['message'] = f'El fantasy standing con el id: {id} no existe en nuestro registros'
        return response_body, 404
    if request.method == 'GET':
        response_body['results'] = row.serialize()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200
    if request.method == 'PUT':
        data = request.json
        row = update_fantasy_standing(row, data.get('fantasy_team_id'))
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = f'Respuesta desde el {request.method} para el id: {id}'
        return response_body, 200


"""
    CRUD /fantasy-coaches
    
    GET /: Obtiene todos los fantasy coaches
    POST /: Añade un fantasy coach
        Ejemplo de body: {"coach_id": 1,
                          "fantasy_team_id": 1}
    GET /<id>: Obtiene un fantasy coach mediante su ID
    PUT /<id>: Actualiza un fantasy coach
        Ejemplo de body: {"fantasy_team_id": 2,
                          "points": 1,
                          "market_value": 123456789,
                          "clause_value": 987654321}
    DELETE /<id>: Elimina un fantasy coach (hard delete)
"""
@api.route('/fantasy-coaches', methods=['GET', 'POST'])
def fantasy_coaches():
    response_body = {}
    if request.method == 'GET':
        result = get_fantasy_coaches()
        response_body['message'] = "List of fantasy coaches"
        response_body['results'] = result
        return response_body, 200
    
    if request.method == 'POST':
        data = request.json
        new_coach = add_fantasy_coach(
            coach_id = data.get('coach_id'),
            fantasy_team_id = data.get('fantasy_team_id'))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = new_coach.serialize()
        return response_body, 201


@api.route('/fantasy-coaches/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def fantasy_coach(id):
    response_body = {}
    fantasy_coach = get_fantasy_coach(id=id)
    if not fantasy_coach:
        response_body['message'] = "Fantasy coach not found"
        return response_body, 404
    
    if request.method == 'GET':
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_coach.serialize()
        return response_body, 200
    
    if request.method == 'PUT':
        data = request.json
        fantasy_coach = update_fantasy_coach(fantasy_coach=fantasy_coach,
                                             fantasy_team_id=data.get("fantasy_team_id"),
                                             points=data.get("points"),
                                             market_value=data.get("market_value"),
                                             clause_value=data.get("clause_value"))
        response_body['message'] = f'Respuesta desde {request.method}'
        response_body['results'] = fantasy_coach.serialize()
        return response_body, 200
    
    if request.method == 'DELETE':
        db.session.delete(fantasy_coach)
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
