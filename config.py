class Config:
    DEBUG = True
    SECRET_KEY = "random-key-word"
    # MySQL Database Config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Dangermouse180@localhost/user_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
