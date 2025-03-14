"""empty message

Revision ID: 56ecd780fc17
Revises: 
Create Date: 2025-03-11 18:48:02.886193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56ecd780fc17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fantasy_leagues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('money', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('coaches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('nationality', sa.String(length=50), nullable=True),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.uid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('fantasy_teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('formation', sa.String(length=20), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=True),
    sa.Column('away_team_id', sa.Integer(), nullable=True),
    sa.Column('home_goals', sa.Integer(), nullable=False),
    sa.Column('away_goals', sa.Integer(), nullable=False),
    sa.Column('is_home_winner', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['teams.uid'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['teams.uid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('nationality', sa.String(length=50), nullable=False),
    sa.Column('position', sa.String(length=50), nullable=False),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.uid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('standings',
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('games_won', sa.Integer(), nullable=False),
    sa.Column('games_draw', sa.Integer(), nullable=False),
    sa.Column('games_lost', sa.Integer(), nullable=False),
    sa.Column('goals_for', sa.Integer(), nullable=False),
    sa.Column('goals_against', sa.Integer(), nullable=False),
    sa.Column('form', sa.String(length=5), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.uid'], ),
    sa.PrimaryKeyConstraint('rank')
    )
    op.create_table('fantasy_coaches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('coach_id', sa.Integer(), nullable=True),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('market_value', sa.Integer(), nullable=False),
    sa.Column('clause_value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['coach_id'], ['coaches.uid'], ),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fantasy_league_teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fantasy_league_id', sa.Integer(), nullable=True),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fantasy_league_id'], ['fantasy_leagues.id'], ),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_teams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fantasy_players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('market_value', sa.Integer(), nullable=False),
    sa.Column('clause_value', sa.Integer(), nullable=False),
    sa.Column('is_scoutable', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_teams.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fantasy_standings',
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('fantasy_team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fantasy_team_id'], ['fantasy_teams.id'], ),
    sa.PrimaryKeyConstraint('rank')
    )
    op.create_table('match_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('time_elapsed', sa.Integer(), nullable=False),
    sa.Column('extra_time_elapsed', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('assist_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('detail', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['assist_id'], ['players.uid'], ),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.uid'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('detail'),
    sa.UniqueConstraint('type'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('match_players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('minutes', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('dribbles_attemps', sa.Integer(), nullable=False),
    sa.Column('dribbles_success', sa.Integer(), nullable=False),
    sa.Column('dribbles_past', sa.Integer(), nullable=False),
    sa.Column('fouls_drawn', sa.Integer(), nullable=False),
    sa.Column('fouls_comitted', sa.Integer(), nullable=False),
    sa.Column('cards_yellow', sa.Integer(), nullable=False),
    sa.Column('cards_red', sa.Integer(), nullable=False),
    sa.Column('penalty_commited', sa.Integer(), nullable=False),
    sa.Column('passes_accuracy', sa.Integer(), nullable=False),
    sa.Column('tackles_total', sa.Integer(), nullable=False),
    sa.Column('tackles_blocks', sa.Integer(), nullable=False),
    sa.Column('tackles_interceptions', sa.Integer(), nullable=False),
    sa.Column('duels_total', sa.Integer(), nullable=False),
    sa.Column('duels_won', sa.Integer(), nullable=False),
    sa.Column('penalty_scored', sa.Integer(), nullable=False),
    sa.Column('penalty_saved', sa.Integer(), nullable=False),
    sa.Column('offsides', sa.Integer(), nullable=False),
    sa.Column('goals_total', sa.Integer(), nullable=False),
    sa.Column('goals_concedes', sa.Integer(), nullable=False),
    sa.Column('goals_assistes', sa.Integer(), nullable=False),
    sa.Column('goals_saved', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['match_id'], ['matches.uid'], ),
    sa.ForeignKeyConstraint(['player_id'], ['players.uid'], ),
    sa.ForeignKeyConstraint(['team_id'], ['teams.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('match_players')
    op.drop_table('match_events')
    op.drop_table('fantasy_standings')
    op.drop_table('fantasy_players')
    op.drop_table('fantasy_league_teams')
    op.drop_table('fantasy_coaches')
    op.drop_table('standings')
    op.drop_table('players')
    op.drop_table('matches')
    op.drop_table('fantasy_teams')
    op.drop_table('coaches')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('fantasy_leagues')
    # ### end Alembic commands ###
