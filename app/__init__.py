from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ORM - Object Relational Mapper - flask-sqlalchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

from .import routes, models

# C - POST
# R - GET
# U - PUT/PATCH
# D - DELETE