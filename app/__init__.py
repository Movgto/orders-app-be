from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import register_blueprints
from app.db import db
from flask_migrate import Migrate
from app.auth import jwt


def create_app(config_object: Config = Config()):
    app = Flask(__name__)
    cors = CORS()
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config.get(
        'CORS_ORIGINS', 'localhost:5000'))

    # Ensure models are imported so SQLAlchemy metadata is populated.
    # This is required for Alembic/Flask-Migrate autogenerate to detect
    # model changes. Use import_module to avoid shadowing the local
    # variable named `app`.
    import importlib
    importlib.import_module('app.models')

    migrate = Migrate()

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    register_blueprints(app)

    return app
