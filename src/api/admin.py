import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, Users, FantasyCoaches, FantasyPlayers, FantasyLeagueTeams, FantasyLeagues, FantasyStandings, FantasyTeams, Teams, Coaches, Players, Standings, Matches, MatchEvents


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(FantasyCoaches, db.session))
    admin.add_view(ModelView(FantasyPlayers, db.session))
    admin.add_view(ModelView(FantasyLeagueTeams, db.session))
    admin.add_view(ModelView(FantasyLeagues, db.session))
    admin.add_view(ModelView(FantasyStandings, db.session))
    admin.add_view(ModelView(FantasyTeams, db.session))
    admin.add_view(ModelView(Teams, db.session))
    admin.add_view(ModelView(Coaches, db.session))
    admin.add_view(ModelView(Players, db.session))
    admin.add_view(ModelView(Standings, db.session))
    admin.add_view(ModelView(Matches, db.session))
    admin.add_view(ModelView(MatchEvents, db.session))
