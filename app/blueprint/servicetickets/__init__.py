from flask import Blueprint

servicetickets_bp = Blueprint('servicetickets_bp', __name__)


from . import routes