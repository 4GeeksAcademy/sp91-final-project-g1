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
                'is_active': self.is_active}


class matches_events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, unique=True, nullable=False)
    time_elapsed = db.Column(db.Integer, unique=False, nullable=False)
    extra_time_elapsed = db.Column(db.Integer, unique=False, nullable=False)
    team_id = db.Column(db.Integer, unique=True, nullable=False)
    player_id = db.Column(db.Integer, unique=True, nullable=False)
    assist_id = db.Column(db.Integer, unique=True, nullable=False)
    type = db.Column(db.String(), unique=True, nullable=False)
    match_id = db.Column(db.String(), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.id} - {self.match_id}>'

    def serialize(self):
        return {"id":self.id,
                "match_id": self.match_id,
                "time_elapsed": self.time_elapsed,
                "extra_time_elapsed": self.extra_time_elapsed,
                "team_id": self.team_id,
                "payer_id":self.player_id,
                "assist_id": self.assist_id,
                "type": self.type,
                "detail": self.detail}


class standings(db.Model):
    rank = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, unique=True, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)
    games_won = db.Column(db.Integer, unique=False, nullable=False)
    games_draw = db.Column(db.Integer,  unique=False, nullable=False)
    games_lost = db.Column(db.Integer,  unique=False, nullable=False)
    goals_for = db.Column(db.Integer,  unique=False, nullable=False)
    goals_against = db.Column(db.Integer,  unique=False, nullable=False)
    form = db.Column(db.String(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.rank} - {self.team_id}>'
 
    def serialize(self):
        return {"rank":self.rank,
                "team_id": self.team_id,
                "points": self.points,
                "games_won": self.games_won,
                "games_draw": self.games_draw,
                "games_lost":self.games_lost,
                "goals_for": self.goals_for,
                "goals_against": self.goals_against,
                "form": self.form}
    

class matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    home_team_id = db.Column(db.Integer, unique=False, nullable=False)
    away_team_id = db.Column(db.Integer, unique=False, nullable=False)
    home_goals = db.Column(db.Integer, unique=True, nullable=False)
    away_goals = db.Column(db.Integer, unique=False, nullable=False)
    is_home_winner = db.Column(db.Boolean, unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.id} - {self.date}>'

    def serialize(self):
        return {"id":self.id,
                "date": self.date,
                "home_team_id": self.home_team_id,
                "away_team_id": self.away_team_id,
                "home_goals": self.home_goals,
                "away_goals":self.away_goals,
                "is_home_winner": self.is_home_winner}
                 