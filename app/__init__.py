from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprint.customers import customers_bp
from app.blueprint.mechanics import mechanics_bp
from app.blueprint.servicetickets import servicetickets_bp
from app.blueprint.inventory import inventory_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.yaml'

swaggerui_blueprint= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop Management API"
    }
)


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    # add extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)



    #registering Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(servicetickets_bp, url_prefix='/servicetickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


    return app
