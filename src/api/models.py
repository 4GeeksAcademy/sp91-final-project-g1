from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)

    def __repr__(self):
        return f'<User {self.username} - {self.email}>'

    def serialize(self):
        # do not serialize the password, its a security breach
        return {"id": self.id,
                "username": self.username,
                "email": self.email,
                "is_active": self.is_active,
                "phone_number": self.phone_number}


class FantasyStandings(db.Model):
    __tablename__ = "fantasy_standings"

    rank = db.Column(db.Integer, primary_key=True)
    # fantasy_team_id = 

    def __repr__(self):
        return f'<FantasyStanding {self.rank} - {self.fantasy_team_id}>'
    
    def serialize(self):
        return {"rank": self.rank,
                "fantasy_team_id": self.fantasy_team_id}


class FantasyLeagues(db.Model):
    __tablename__ = "fantasy_league"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    photo = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return f'<FantasyLeague {self.id} - {self.name}>'
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "photo": self.photo}


class FantasyLeagueTeams(db.Model):
    __tablename__ = "fantasy_league_teams"

    id = db.Column(db.Integer, primary_key=True)
    # fantasy_league_id = 
    # fantasy_team_id = 

    def __repr__(self):
        return f'<FantasyLeagueTeam {self.fantasy_team_id} - {self.fantasy_league_id}>'
    
    def serialize(self):
        return {"id": self.id,
                "fantasy_league_id": self.fantasy_league_id,
                "fantasy_team_id": self.fantasy_team_id}


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    logo = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return f'<Team {self.id} - {self.name}>'
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "photo": self.photo}


class Coaches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    nationality = db.Column(db.String(50), unique=False, nullable=False)
    photo = db.Column(db.String(255), unique=False, nullable=True)
    #team_id = 

    def __repr__(self):
        return f'<Coach {self.id} - {self.name}>'
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "nationality": self.nationality,
                "photo": self.photo,
                "team_id": self.team_id}

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    nationality = db.Column(db.String(50), unique=False, nullable=False)
    position = db.Column(db.String(50), unique=False, nullable=False)
    photo = db.Column(db.String(255), unique=False, nullable=True)
    #team_id = 

    def __repr__(self):
        return f'<Player {self.id} - {self.name}>'
    
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "number": self.number,
                "nationality": self.nationality,
                "position": self.position,
                "photo": self.photo,
                "team_id": self.team_id}    
class FantasyCoach(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # coach_id  
    # fantasy_team_id 
    points = db.Column(db.Integer, unique=False, nullable=False)
    market_value = db.Column(db.Integer, unique=False, nullable=False)
    clause_value = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'FantasyCoach: {self.coach_id} - {self.market_value}'
    
    def serialize(self):
        return {
            "id": self.id,
            # "coach_id": self.coach_id,
            # "fantasy_team_id": self.fantasy_team_id,
            "points": self.points,
            "market_value": self.market_value,
            "clause_value": self.clause_value,
        }
    
class FantasyTeam(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id 
    name = db.Column(db.String(), unique=False, nullable=False)
    logo = db.Column(db.String(), unique=False, nullable=True)
    formation = db.Column(db.String(), unique=False, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'FantasyTeam: {self.id} - {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            # "user_id": self.user_id,
            "name": self.name,
            "logo": self.logo,
            "formation": self.formation,
            "points": self.points,
        }
    
class FantasyPlayer(db.model):
    id = db.Column(db.Integer, primary_key=True)
    # player_id 
    # fantasy_team_id 
    position = db.Column(db.Integer, unique=False, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)
    market_value = db.Column(db.Integer, unique=False, nullable=False)
    clause_value = db.Column(db.Integer, unique=False, nullable=False)
    is_scoutable = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return f'FantasyPlayer: {self.id} - {self.player_id}'
    
    def serialize(self):
        return {
            "id": self.id,
            # "player_id": self.player_id,
            # "fantasy_team_id": self.fantasy_team_id,
            "position": self.position,
            "points": self.points,
            "market_value": self.market_value,
            "clause_value": self.clause_value,
            "is_scoutable": self.is_scoutable,
        }
