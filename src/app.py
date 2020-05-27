import os
import problem, board

from flask import Flask
from extensions import db, migrate, cors

app = {}

def create_app():
    database_url = os.getenv('DATABASE_URL')

    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

def register_blueprints(app):
    origins = '*'
    cors.init_app(problem.views.blueprint, origins=origins)
    cors.init_app(board.views.blueprint, origins=origins)

    app.register_blueprint(problem.views.blueprint)
    app.register_blueprint(board.views.blueprint)

if __name__ == '__main__':
    app = create_app()
    app.run(host= '0.0.0.0')