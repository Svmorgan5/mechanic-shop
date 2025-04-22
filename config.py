class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:ABC123@localhost/MECHANIC_SHOP_db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'



class TestingConfig:
    pass

class ProductionConfig:
    pass

