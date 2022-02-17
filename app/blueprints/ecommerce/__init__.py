from flask import Blueprint

bp = Blueprint('ecommerce', __name__, url_prefix='/shop')

from .import routes, models