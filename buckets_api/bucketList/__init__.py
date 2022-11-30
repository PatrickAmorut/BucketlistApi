from flask import Flask 
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from bucketList.auth.resource import auth
from bucketList.bk_list.items import buckets
from bucketList.models import db
# from flask_restful import Api


# api = Api()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
Login_manager = LoginManager()



def create_app():
    # create flask instance 
    app = Flask(__name__)
    # database  configuration
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/api_bucket' #'sqlite:///site.db'
    

    # api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    Login_manager.init_app(app)
    
    # registering blueprints 
    app.register_blueprint(auth)
    app.register_blueprint(buckets)

    return app



