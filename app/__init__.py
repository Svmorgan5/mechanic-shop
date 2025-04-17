from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprint.customers import customers_bp
from app.blueprint.mechanics import mechanics_bp
from app.blueprint.servicetickets import servicetickets_bp

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    # add extensions
    db.init_app(app)
    ma.init_app(app)

    #registering Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(servicetickets_bp, url_prefix='/servicetickets')

    return app
