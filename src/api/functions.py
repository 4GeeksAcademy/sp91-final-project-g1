from api.models import db, Teams, Matches, Coaches, Players, FantasyCoaches, FantasyTeams, FantasyPlayers, Users, FantasyLeagues, FantasyStandings, FantasyLeagueTeams, Standings
import bcrypt
from typing import List


"""
    ======================================================
    ======================================================
    ================  Funciones users ====================
    ======================================================
    ======================================================
"""
def get_users():
    rows = db.session.execute(db.select(Users)).scalars()
    result = [ row.serialize() for row in rows]
    return result


def get_user_by_id(id) -> Users:
    return db.session.get(Users, id)


def get_user_by_email(email) -> Users:
    row = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
    return row


def get_active_user_by_email(email) -> Users:
    row = db.session.execute(db.select(Users).where(Users.email == email, Users.is_active == True)).scalar()
    return row


def generate_password_hash(password):
    bytes = str(password).encode('utf-8')
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode("utf-8")


def add_user(username, email, password, phone_number):
    hash_password = generate_password_hash(password)
    new_user = Users(username = username, 
                     email = email, 
                     password = hash_password, 
                     phone_number = phone_number, 
                     is_active = True)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def update_user(user: Users, username, email, phone_number):
    user.username = username
    user.email = email
    user.phone_number = phone_number
    db.session.commit()
    return user


def delete_user(user=Users):
    user.is_active = False
    db.session.commit()


def get_fantasy_team_by_user_id(id) -> FantasyTeams:
    row = db.session.execute(db.select(FantasyTeams).where(FantasyTeams.user_id == id)).scalar()
    return row


def add_user_to_league(user_id, league_id):
    fantasy_team = get_fantasy_team_by_user_id(user_id)
    fantasy_league = get_fantasy_league(league_id)
    new_team_of_league = FantasyLeagueTeams(
        fantasy_league_id=int(fantasy_league.id),
        fantasy_team_id=int(fantasy_team.id)
    )
    db.session.add(new_team_of_league)
    db.session.commit()
    return new_team_of_league


"""
    ======================================================
    ======================================================
    ================  Funciones teams ====================
    ======================================================
    ======================================================
"""
def get_teams():
    rows = db.session.execute(db.select(Teams)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_team(uid, name, logo):
    new_team = Teams(
            uid = uid,
            name = name,
            logo = logo)
    db.session.add(new_team)
    db.session.commit()
    return new_team.serialize()


"""
    ======================================================
    ======================================================
    ===============  Funciones matches ===================
    ======================================================
    ======================================================
"""
def get_matches():
    rows = db.session.execute(db.select(Matches)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_match(date, home_team_id, away_team_id, home_goals, away_goals, is_home_winner):
    new_match = Matches(
        date = date,
        home_team_id = home_team_id,
        away_team_id = away_team_id,
        home_goals = home_goals,
        away_goals = away_goals,
        is_home_winner = is_home_winner)
    db.session.add(new_match)
    db.session.commit()
    return new_match.serialize()


"""
    ======================================================
    ======================================================
    ==============  Funciones standings ==================
    ======================================================
    ======================================================
"""
def get_standings():
    rows = db.session.execute(db.select(Standings)).scalars()
    result = [ row.serialize() for row in rows ]
    return result


def add_standing(team_id, points, games_won, games_draw, games_lost, goals_for, goals_against, form):
    new_standing = Standings(
            team_id = team_id,
            points = points,
            games_won = games_won,
            games_draw = games_draw,
            games_lost = games_lost,
            goals_for = goals_for,
            goals_against = goals_against,
            form = form)
    db.session.add(new_standing)
    db.session.commit()
    return new_standing


def update_standing(team_id, points, games_won, games_draw, games_lost, goals_for, goals_against, form):
    standing = db.session.execute(db.select(Standings).where(Standings.team_id == team_id)).scalar()
    standing.team_id = team_id
    standing.points = points
    standing.games_won = games_won
    standing.games_draw = games_draw
    standing.games_lost = games_lost
    standing.goals_for = goals_for
    standing.goals_against = goals_against
    standing.form = form
    db.session.commit()
    return standing


def initialize_standings(create_new=False):
    teams_data = get_teams()
    data = []
    for team_data in teams_data:
        if create_new == True:
            new_standing = add_standing(
            team_id = team_data['uid'],
            points = 0,
            games_won = 0,
            games_draw = 0,
            games_lost = 0,
            goals_for = 0,
            goals_against = 0,
            form = '')
        else:
            new_standing = update_standing(
                team_id = team_data['uid'],
                points = 0,
                games_won = 0,
                games_draw = 0,
                games_lost = 0,
                goals_for = 0,
                goals_against = 0,
                form = '')
        data.append(new_standing)
    return data


def calculate_standings(today): 
    rows_matches = db.session.execute(db.select(Matches).where(Matches.date <= today).order_by(Matches.date)).scalars()
    matches_today = [match_today.serialize() for match_today in rows_matches]
    teams_data = get_standings()
    for match in matches_today:
        home_team = next(team_data for team_data in teams_data if team_data['team_id'] == match['home_team_id'])
        away_team = next(team_data for team_data in teams_data if team_data['team_id'] == match['away_team_id'])
        home_team['goals_for'] += match['home_goals']
        home_team['goals_against'] += match['away_goals']
        away_team['goals_for'] += match['away_goals']
        away_team['goals_against'] += match['home_goals']
        if match['home_goals'] > match['away_goals']:
            home_team['points'] += 3
            home_team['games_won'] += 1
            home_team['form'] += "V"
            away_team['games_lost'] += 1
            away_team['form'] += "D"
        elif match['home_goals'] == match['away_goals']:
            home_team['points'] += 1
            home_team['form'] += "E"
            home_team['games_draw'] += 1
            away_team['points'] += 1
            away_team['form'] += "E"
            away_team['games_draw'] += 1
        else:
            away_team['points'] += 3
            away_team['form'] += "V"
            away_team['games_won'] += 1
            home_team['form'] += "D"
            home_team['games_lost'] += 1
        
        if len(home_team['form']) > 5:
            home_team['form'] = home_team['form'][:5]
        if len(away_team['form']) > 5:
            away_team['form'] = away_team['form'][:5]
    return teams_data


"""
    ======================================================
    ======================================================
    ===============  Funciones coaches ===================
    ======================================================
    ======================================================
"""
def get_coaches():
    rows = db.session.execute(db.select(Coaches)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_coach(uid, name, first_name, last_name, nationality, photo, team_id):
    new_coach = Coaches(
        uid = uid,
        name = name,
        first_name = first_name,
        last_name = last_name,
        nationality = nationality,
        photo = photo,
        team_id = team_id)
    db.session.add(new_coach)
    db.session.commit()
    return new_coach.serialize()


def get_coach_by_id(id) -> Coaches:
    return db.session.get(Coaches, id)


"""
    ======================================================
    ======================================================
    ================ Funciones players ===================
    ======================================================
    ======================================================
"""
def get_players():
    rows = db.session.execute(db.select(Players)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_player(name, first_name, last_name, number, nationality, position, photo, team_id):
    new_player = Players(
        name = name,
        first_name = first_name,
        last_name = last_name,
        number = number,
        nationality = nationality,
        position = position,
        photo = photo,
        team_id = team_id)
    db.session.add(new_player)
    db.session.commit()
    return new_player


"""
    ======================================================
    ======================================================
    ================ Funciones market ====================
    ======================================================
    ======================================================
"""
# TODO: Esta función va mal a veces
def get_players_market(page, limit):
    players_rows = db.session.execute(db.select(Players).limit(limit).offset(int(page)*int(limit))).scalars()

    def serialize(row):
        serialized_row = row.serialize()
        team_row = db.session.execute(db.select(Teams).where(Teams.uid == row.team_id)).scalar()
        if team_row == None:
            return serialized_row
        team = team_row.serialize()
        serialized_row["team"] = team
        fantasy_player = get_fantasy_player_with_team_data(row.uid)
        serialized_row['fantasy_team'] = fantasy_player['fantasy_team'] if fantasy_player is not None else None
        return serialized_row

    result = [serialize(row) for row in players_rows]
    return result


"""
    ======================================================
    ======================================================
    ============ Funciones fantasy leagues ===============
    ======================================================
    ======================================================
"""
def get_fantasy_leagues():
    rows = db.session.execute(db.select(FantasyLeagues)).scalars()
    result = [ row.serialize() for row in rows]
    return result


def add_fantasy_league(name, photo):
    new_league = FantasyLeagues(name=name,
                                photo=photo)     
    db.session.add(new_league)
    db.session.commit()
    return new_league


def get_fantasy_league(id) -> FantasyLeagues: 
    return db.session.get(FantasyLeagues, id)


def update_fantasy_league(fantasy_league: FantasyLeagues, name: str, photo: str):
    fantasy_league.name = name
    fantasy_league.photo = photo
    db.session.commit()
    return fantasy_league


"""
    ======================================================
    ======================================================
    ========= Funciones fantasy league teams =============
    ======================================================
    ======================================================
"""
def get_fantasy_league_teams():
    rows = db.session.execute(db.select(FantasyLeagueTeams)).scalars()
    result = [ row.serialize() for row in rows]
    return result


def add_fantasy_league_team(fantasy_team_id, fantasy_league_id):
    new_league_team = FantasyLeagueTeams(fantasy_team_id=fantasy_team_id,
                                         fantasy_league_id=fantasy_league_id)     
    db.session.add(new_league_team)
    db.session.commit()
    return new_league_team


def get_fantasy_league_team_by_id(id) -> FantasyLeagueTeams:
    return db.session.get(FantasyLeagueTeams, id)


def update_fantasy_league_team(fantasy_league_team: FantasyLeagueTeams, fantasy_team_id, fantasy_league_id):
    fantasy_league_team.fantasy_team_id = fantasy_team_id
    fantasy_league_team.fantasy_league_id = fantasy_league_id
    db.session.commit()
    return fantasy_league_team


"""
    ======================================================
    ======================================================
    ========== Funciones fantasy standings ===============
    ======================================================
    ======================================================
"""
#TODO: Calcular standings
def get_fantasy_standings():
    rows = db.session.execute(db.select(FantasyStandings)).scalars()
    result = [ row.serialize() for row in rows]
    return result


def add_fantasy_standing(fantasy_team_id):
    new_standing = FantasyStandings(fantasy_team_id=fantasy_team_id)
    db.session.add(new_standing)
    db.session.commit()
    return new_standing


def get_fantasy_standing(id) -> FantasyStandings:
    return db.session.get(FantasyStandings, id)


def update_fantasy_standing(fantasy_standing: FantasyStandings, fantasy_team_id):
    fantasy_standing.fantasy_team_id = fantasy_team_id
    db.session.commit()
    return fantasy_standing


"""
    ======================================================
    ======================================================
    ============ Funciones fantasy coaches ===============
    ======================================================
    ======================================================
"""
def get_fantasy_coaches():
    rows = db.session.execute(db.select(FantasyCoaches)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_fantasy_coach(coach_id, fantasy_team_id):
    new_coach = FantasyCoaches(
            coach_id = coach_id,
            fantasy_team_id = fantasy_team_id,
            points = 0,
            market_value = 0,
            clause_value = 0)
    db.session.add(new_coach)
    db.session.commit()
    return new_coach


def get_fantasy_coach(id) -> FantasyCoaches:
    return db.session.get(FantasyCoaches, id)


def update_fantasy_coach(fantasy_coach: FantasyCoaches, fantasy_team_id, points, market_value, clause_value):
    fantasy_coach.fantasy_team_id = fantasy_team_id
    fantasy_coach.points = points
    fantasy_coach.market_value = market_value
    fantasy_coach.clause_value = clause_value
    db.session.commit()
    return fantasy_coach


"""
    ======================================================
    ======================================================
    ============= Funciones fantasy teams ================
    ======================================================
    ======================================================
""" 
def get_fantasy_teams():
    rows = db.session.execute(db.select(FantasyTeams)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_fantasy_team(user_id, name, logo):
    new_team = FantasyTeams(
        user_id = user_id,
        name = name,
        logo = logo,
        formation = "4-3-3",
        points = 0)
    db.session.add(new_team)
    db.session.commit()
    return new_team


def get_fantasy_team_by_id(id) -> FantasyTeams:
    return db.session.get(FantasyTeams, id)


def update_fantasy_team(fantasy_team: FantasyTeams, name, logo, formation, points):
    fantasy_team.name = name
    fantasy_team.logo = logo
    fantasy_team.formation = formation
    fantasy_team.points = points
    db.session.commit()
    return fantasy_team


"""
    ======================================================
    ======================================================
    ============ Funciones fantasy players ===============
    ======================================================
    ======================================================
"""
def get_fantasy_players_by_team(id):
    rows = db.session.execute(db.select(FantasyPlayers).where(FantasyPlayers.fantasy_team_id == id)).scalars()
    data = []
    for row in rows:
        item = row.serialize()
        player = db.session.execute(db.select(Players).where(Players.uid == item['player_id'])).scalar().serialize()
        item['name'] = player['name']
        item['photo'] = player['photo']
        data.append(item)
    return data


def get_fantasy_players():
    rows = db.session.execute(db.select(FantasyPlayers)).scalars()
    result = [row.serialize() for row in rows]
    return result


def add_fantasy_player(player_id, fantasy_team_id, position, clause_value):
    new_player = FantasyPlayers(
        player_id = player_id,
        fantasy_team_id = fantasy_team_id,
        position = position,
        points = 0,
        clause_value = clause_value)
    db.session.add(new_player)
    db.session.commit()
    return new_player


def get_fantasy_player_by_id(id) -> FantasyPlayers:
    return db.session.get(FantasyPlayers, id)


def get_fantasy_player_by_player_id(id) -> FantasyPlayers:
    return db.session.execute(db.select(FantasyPlayers).where(FantasyPlayers.player_id == id)).scalar()


def update_fantasy_player(fantasy_player: FantasyPlayers, fantasy_team_id, points, clause_value, is_scoutable):
    fantasy_player.fantasy_team_id = fantasy_team_id
    fantasy_player.points = points
    fantasy_player.clause_value = clause_value
    fantasy_player.is_scoutable = is_scoutable
    db.session.commit()
    return fantasy_player


def get_fantasy_player_with_team_data(id):
    fantasy_player = get_fantasy_player_by_player_id(id=id)
    if fantasy_player is None:
        return None
    fantasy_team_data = get_fantasy_team_by_id(id=fantasy_player.fantasy_team_id)
    fantasy_player = fantasy_player.serialize()
    fantasy_player['fantasy_team'] = fantasy_team_data.serialize()
    return fantasy_player
