from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ORM - Object Relational Mapper - flask-sqlalchemy
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    login_manager.init_app(app)

    # Register the blueprints
    from app.blueprints.blog import bp as blog
    from app.blueprints.main import bp as main
    from app.blueprints.authentication import bp as authentication
    from app.blueprints.api import bp as api
    app.register_blueprint(blog)
    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(authentication)

    with app.app_context():
        from app.blueprints.ecommerce import bp as ecommerce
        app.register_blueprint(ecommerce)
        # from app.blueprints.ecommerce import routes

    return app

# C - POST
# R - GET
# U - PUT/PATCH
# D - DELETE