from flask import Flask
from app.models import db
from app.extensions import ma, limiter, cache
from app.blueprint.customers import customers_bp
from app.blueprint.mechanics import mechanics_bp
from app.blueprint.servicetickets import servicetickets_bp
from app.blueprint.inventory import inventory_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    # add extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #Gloabal Limiter

  
    #registering Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(servicetickets_bp, url_prefix='/servicetickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')


    return app
