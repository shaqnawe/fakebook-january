from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api/v1')

from .import authentication, blog, ecommerce