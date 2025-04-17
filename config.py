class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:ABC123@localhost/MECHANIC_SHOP_db'
    DEBUG = True



class TestingConfig:
    pass

class ProductionConfig:
    pass

