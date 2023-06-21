from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.pc_bp import pcs_bp
from blueprints.part_bp import parts_bp
from blueprints.pc_build_part_bp import pc_build_part_bp
from marshmallow.exceptions import ValidationError

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://db_dev:crazyshadow@localhost:5432/pc_build_db"
    app.config['JWT_SECRET_KEY'] = "backwardsforwards"

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pcs_bp)
    app.register_blueprint(parts_bp)
    app.register_blueprint(pc_build_part_bp)

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': f'{err}'}, 401

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.__dict__['messages']}, 400


    return app