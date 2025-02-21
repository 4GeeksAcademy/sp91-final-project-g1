"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import requests
import dotenv
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Teams, Matches, Coaches, Players, FantasyCoaches, FantasyTeams, FantasyPlayers, Users, FantasyLeagues, FantasyStandings, FantasyLeagueTeams


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API
dotenv.load_dotenv()

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return response_body, 200

@api.route('/populate-db-1', methods=['GET'])
def populate_db():
    # Paso 1: Llamar a /teams
    teams_url = f'https://{os.getenv("API_URL")}/teams' # TODO: eliminar /api, esta puesto para que falle, que no gaste peticiones
    params = { "league": 140, "season": 2023}
    headers = { "x-rapidapi-host": os.getenv("API_URL"),
                "x-rapidapi-key": os.getenv("API_KEY") }
    result = requests.get(teams_url, params=params, headers=headers)
    rows = result.json().get('response')
    print(result.json())
    for row in rows:
        # Paso 1.2: Subir los teams a BDD
        team = row.get('team')
        new_team = Teams(
            uid = team.get('id'),
            name = team.get('name'),
            logo = team.get('logo'))
        # db.session.add(new_team)
        # Paso 1.3: Llamar a coachs/:team (:team = id del row actual)
        coach_url = f'https://{os.getenv("API_URL")}/api/coachs'
        params = { "team": team.get('id')}
        headers = { "x-rapidapi-host": os.getenv("API_URL"),
                    "x-rapidapi-key": os.getenv("API_KEY") }
        result = requests.get(coach_url, params=params, headers=headers)
        rows = result.json().get('response')
        for row in rows:
        # Paso 1.3.1: Subir el coach que esté en la temporada 23-24 a BDD
            """new_coach = Coaches(
                name = row.get('name'),
                first_name = row.get('first_name'),
                last_name = row.get('last_name'),
                nationality = row.get('nationality'),
                photo = row.get('photo'),
                team_id = row.get('team_id'))
            db.session.add(new_coach)"""
            pass
    # Paso 2: Llamar a /fixtures
        fixtures_url = f'https://{os.getenv("API_URL")}/fixtures'
        params = { "league": 140, "season": 2023}
        headers = { "x-rapidapi-host": os.getenv("API_URL"),
                    "x-rapidapi-key": os.getenv("API_KEY") }
        result = requests.get(fixtures_url, params=params, headers=headers)
        rows = result.json().get('response')
        print(result.json())
        for row in rows:
        # Paso 1.2: Subir los teams a BDD
            fixture = row.get('fixture')
            teams = row.get('teams')
            goals = row.get('goals')
            home_team = teams.get('home')
            away_team = teams.get('away')
            home_goals = goals.get('home')
            away_goals = goals.get('away')
            new_fixture = Matches(
                uid = fixture.get('id'),
                date = fixture.get('date'),
                home_team_id = home_team.get('id'),
                away_team_id = away_team.get('id'),
                home_goals = home_goals,
                away_goals = away_goals,
                is_home_winner = home_goals > away_goals)
            db.session.add(new_fixture)
        # PASO 2.2: Subir las fixtures a BDD
    db.session.commit()
    print("Base de datos actualizada correctamente")
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
