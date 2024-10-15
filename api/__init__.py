from flask import Flask
from .extensions import db, migrate
from .routes import main
from .extensions import SQLALCHEMY_DATABASE_URI

def create_api():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main)

    return app
