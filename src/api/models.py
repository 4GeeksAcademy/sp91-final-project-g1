from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
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


class FantasyTeams(db.Model):
    __tablename__ = "fantasy_teams"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id")) 
    name = db.Column(db.String(50), unique=False, nullable=False) #TODO: A la hora de crear un equipo, comprobar que el nombre sea unico para la misma liga
    logo = db.Column(db.String(255), unique=False, nullable=True)
    formation = db.Column(db.String(20), unique=False, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)
    user_to = db.relationship('Users', foreign_keys=[user_id], backref=db.backref('fantasy_team_of_user', lazy='select'))

    def __repr__(self):
        return f'<FantasyTeam: {self.id} - {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "logo": self.logo,
            "formation": self.formation,
            "points": self.points,
        }


class FantasyLeagues(db.Model):
    __tablename__ = "fantasy_leagues"

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
    fantasy_league_id = db.Column(db.Integer, db.ForeignKey("fantasy_leagues.id")) 
    fantasy_team_to = db.relationship('FantasyLeagues', foreign_keys=[fantasy_league_id], backref=db.backref('fantasy_league_of', lazy='select'))
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey("fantasy_teams.id")) 
    fantasy_team_to = db.relationship('FantasyTeams', foreign_keys=[fantasy_team_id], backref=db.backref('fantasy_team_in', lazy='select'))

    def __repr__(self):
        return f'<FantasyLeagueTeam {self.fantasy_team_id} - {self.fantasy_league_id}>'
    
    def serialize(self):
        return {"id": self.id,
                "fantasy_league_id": self.fantasy_league_id,
                "fantasy_team_id": self.fantasy_team_id}


class FantasyStandings(db.Model):
    __tablename__ = "fantasy_standings"

    rank = db.Column(db.Integer, primary_key=True)
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey("fantasy_teams.id")) 
    fantasy_team_to = db.relationship('FantasyTeams', foreign_keys=[fantasy_team_id], backref=db.backref('fantasy_rank_of', lazy='select'))

    def __repr__(self):
        return f'<FantasyStanding {self.rank} - {self.fantasy_team_id}>'
    
    def serialize(self):
        return {"rank": self.rank,
                "fantasy_team_id": self.fantasy_team_id}


class FantasyCoaches(db.Model):
    __tablename__ = "fantasy_coaches"

    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey("coaches.uid"))  
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey("fantasy_teams.id")) 
    points = db.Column(db.Integer, unique=False, nullable=False)
    market_value = db.Column(db.Integer, unique=False, nullable=False)
    clause_value = db.Column(db.Integer, unique=False, nullable=False)
    coach_to = db.relationship('Coaches', foreign_keys=[coach_id], backref=db.backref('fantasy_coach_is', lazy='select'))
    fantasy_team_to = db.relationship('FantasyTeams', foreign_keys=[fantasy_team_id], backref=db.backref('fantasy_coach_of', lazy='select'))

    def __repr__(self):
        return f'<FantasyCoach: {self.coach_id} - {self.market_value}>'
    
    def serialize(self):
        return {"id": self.id,
            "coach_id": self.coach_id,
            "fantasy_team_id": self.fantasy_team_id,
            "points": self.points,
            "market_value": self.market_value,
            "clause_value": self.clause_value}

 
class FantasyPlayers(db.Model):
    __tablename__ = "fantasy_players"
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("players.uid")) 
    fantasy_team_id = db.Column(db.Integer, db.ForeignKey("fantasy_teams.id")) 
    position = db.Column(db.Integer, unique=True, nullable=False)
    points = db.Column(db.Integer, unique=False, nullable=False)
    market_value = db.Column(db.Integer, unique=False, nullable=False)
    clause_value = db.Column(db.Integer, unique=False, nullable=False)
    is_scoutable = db.Column(db.Boolean, unique=False, nullable=False)
    player_to = db.relationship('Players', foreign_keys=[player_id], backref=db.backref('fantasy_player_is', lazy='select'))
    fantasy_team_to = db.relationship('FantasyTeams', foreign_keys=[fantasy_team_id], backref=db.backref('fantasy_player_of', lazy='select'))

    def __repr__(self):
        return f'<FantasyPlayer: {self.id} - {self.player_id}>'
    
    def serialize(self):
        return {"id": self.id,
            "player_id": self.player_id,
            "fantasy_team_id": self.fantasy_team_id,
            "position": self.position,
            "points": self.points,
            "market_value": self.market_value,
            "clause_value": self.clause_value,
            "is_scoutable": self.is_scoutable}


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    logo = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return f'<Team {self.uid} - {self.name}>'
    
    def serialize(self):
        return {"uid": self.uid,
                "name": self.name,
                "photo": self.photo}


class Standings(db.Model):
    rank = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.uid"))
    points = db.Column(db.Integer, unique=False, nullable=False)
    games_won = db.Column(db.Integer, unique=False, nullable=False)
    games_draw = db.Column(db.Integer,  unique=False, nullable=False)
    games_lost = db.Column(db.Integer,  unique=False, nullable=False)
    goals_for = db.Column(db.Integer,  unique=False, nullable=False)
    goals_against = db.Column(db.Integer,  unique=False, nullable=False)
    form = db.Column(db.String(5), unique=False, nullable=False)
    team_to = db.relationship('Teams', foreign_keys=[team_id], backref=db.backref('rank_of', lazy='select'))

    def __repr__(self):
        return f'<Standings {self.rank} - {self.team_id}>'
 
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
 

class Coaches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    nationality = db.Column(db.String(50), unique=False, nullable=False)
    photo = db.Column(db.String(255), unique=False, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.uid")) 
    team_to = db.relationship('Teams', foreign_keys=[team_id], backref=db.backref('coach_of', lazy='select'))

    def __repr__(self):
        return f'<Coach {self.uid} - {self.name}>'
    
    def serialize(self):
        return {"uid": self.uid,
                "name": self.name,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "nationality": self.nationality,
                "photo": self.photo,
                "team_id": self.team_id}


class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    number = db.Column(db.Integer, unique=False, nullable=False)
    nationality = db.Column(db.String(50), unique=False, nullable=False)
    position = db.Column(db.String(50), unique=False, nullable=False)
    photo = db.Column(db.String(255), unique=False, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.uid"))
    team_to = db.relationship('Teams', foreign_keys=[team_id], backref=db.backref('player_of', lazy='select'))

    def __repr__(self):
        return f'<Player {self.uid} - {self.name}>'
    
    def serialize(self):
        return {"uid": self.uid,
                "name": self.name,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "number": self.number,
                "nationality": self.nationality,
                "position": self.position,
                "photo": self.photo,
                "team_id": self.team_id}    


class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey("teams.uid"))
    away_team_id = db.Column(db.Integer, db.ForeignKey("teams.uid"))
    home_goals = db.Column(db.Integer, unique=False, nullable=False)
    away_goals = db.Column(db.Integer, unique=False, nullable=False)
    is_home_winner = db.Column(db.Boolean, unique=False, nullable=False)
    home_team_to = db.relationship('Teams', foreign_keys=[home_team_id], backref=db.backref('home_team_is', lazy='select'))
    away_team_to = db.relationship('Teams', foreign_keys=[away_team_id], backref=db.backref('away_team_is', lazy='select'))
    
    def __repr__(self):
        return f'<Match {self.uid} - {self.date}>'

    def serialize(self):
        return {"uid":self.uid,
                "date": self.date,
                "home_team_id": self.home_team_id,
                "away_team_id": self.away_team_id,
                "home_goals": self.home_goals,
                "away_goals":self.away_goals,
                "is_home_winner": self.is_home_winner}


class MatchEvents(db.Model):
    __tablename__ = "match_events"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"))
    time_elapsed = db.Column(db.Integer, unique=False, nullable=False)
    extra_time_elapsed = db.Column(db.Integer, unique=False, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("players.uid"))
    assist_id = db.Column(db.Integer, db.ForeignKey("players.uid"))
    type = db.Column(db.String(255), unique=True, nullable=False)
    detail = db.Column(db.String(255), unique=True, nullable=False)
    match_to = db.relationship('Matches', foreign_keys=[match_id], backref=db.backref('match_of', lazy='select'))
    team_to = db.relationship('Teams', foreign_keys=[team_id], backref=db.backref('team_of', lazy='select'))
    player_to = db.relationship('Players', foreign_keys=[player_id], backref=db.backref('player_of', lazy='select'))
    assist_to = db.relationship('Players', foreign_keys=[assist_id], backref=db.backref('assist_of', lazy='select'))
    
    def __repr__(self):
        return f'<MatchEvents {self.id} - {self.match_id}>'

    def serialize(self):
        return {"uid":self.uid,
                "match_id": self.match_id,
                "time_elapsed": self.time_elapsed,
                "extra_time_elapsed": self.extra_time_elapsed,
                "team_id": self.team_id,
                "payer_id":self.player_id,
                "assist_id": self.assist_id,
                "type": self.type,
                "detail": self.detail}


class MatchPlayers(db.model):
    __tablename__ = "match_players"

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.uid"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.uid"))
    player_id = db.Column(db.Integer, db.ForeignKey("players.uid"))
    minutes = db.Column(db.Integer, unique=False, nullable=False)
    position = db.Column(db.Integer, unique=False, nullable=False)
    dribbles_attemps= db.Column(db.Integer, unique=False, nullable=False)
    dribbles_success= db.Column(db.Integer, unique=False, nullable=False)
    dribbles_past = db.Column(db.Integer, unique=False, nullable=False)
    fouls_drawn = db.Column(db.Integer, unique=False, nullable=False)
    fouls_comitted = db.Column(db.Integer, unique=False, nullable=False)
    cards_yellow= db.Column(db.Integer, unique=False, nullable=False)
    cards_red= db.Column(db.Integer, unique=False, nullable=False)
    penalty_commited= db.Column(db.Integer, unique=False, nullable=False)
    passes_accuracy= db.Column(db.Integer, unique=False, nullable=False)
    tackles_total= db.Column(db.Integer, unique=False, nullable=False)
    tackles_blocks= db.Column(db.Integer, unique=False, nullable=False) 
    tackles_interceptions= db.Column(db.Integer, unique=False, nullable=False) 
    duels_total= db.Column(db.Integer, unique=False, nullable=False) 
    duels_won= db.Column(db.Integer, unique=False, nullable=False) 
    penalty_scored= db.Column(db.Integer, unique=False, nullable=False) 
    penalty_saved= db.Column(db.Integer, unique=False, nullable=False) 
    offsides= db.Column(db.Integer, unique=False, nullable=False) 
    goals_total= db.Column(db.Integer, unique=False, nullable=False) 
    goals_concedes= db.Column(db.Integer, unique=False, nullable=False) 
    goals_assistes= db.Column(db.Integer, unique=False, nullable=False)
    goals_saved= db.Column(db.Integer, unique=False, nullable=False) 
    match_to = db.relationship('Matches', foreign_keys=[match_id], backref=db.backref('match_of', lazy='select'))
    team_to = db.relationship('Teams', foreign_keys=[team_id], backref=db.backref('team_of', lazy='select'))
    player_to = db.relationship('Players', foreign_keys=[player_id], backref=db.backref('player_of', lazy='select'))

    
    def __repr__(self):
        return f'<MatchPlayers {self.match_id} -  {self.player_id}>'

    def serialize(self):
        return {"id":self.id,
                "match_id": self.match_id,
                "team_id": self.team_id,
                "player_id": self.player_id,
                "minutes": self.minutes,
                "position":self.position,
                "dribbles_attemps": self.dribbles_attemps,
                "driblles_success": self.dribbles_success,
                "driblles_past": self.dribbles_past,
                "fouls_drawn": self.fouls_drawn,
                "fouls_comitted": self.fouls_comitted,
                "cards_yellow": self.cards_yellow,
                "cards_red": self.cards_red,
                "penalty_commited": self.penalty_commited,
                "passes_accuracy": self.passes_accuracy,
                "tackles_total": self.tackles_total,
                "tackles_blocks": self.tackles_blocks,
                "tackles_interceptions": self.tackles_interceptions,
                "duels_total": self.duels_total,
                "duels_won": self.duels_won,
                "penalty_scored": self.penalty_scored,
                "penalty_saved": self.penalty_saved,
                "offsides": self.offsides,
                "goals_total": self.goals_total,
                "goals_concedes": self.goals_concedes,
                "goals_assistes": self.goals_assistes,
                "goals_saved": self.goals_saved,}