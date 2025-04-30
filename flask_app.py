from app import create_app
from app.models import db

app = create_app('ProductionConfig')  # Change to 'DevelopmentConfig' or 'TestingConfig' as needed


with app.app_context():
    #db.drop_all()  # Drop all tables if they exist
    db.create_all()
