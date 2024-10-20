from config import Config
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import Engine
from sqlalchemy import event
# from flasgger import Swagger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config.from_object(Config)

security_definitions = {
   "basicAuth": {
       "type": "basic"
   }
}

app.config.update({
   'APISPEC_SPEC': APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions,
        security=[],
        openapi_version='2.0'
   ),
   'APISPEC_SWAGGER_URL': '/swagger', # URI API Doc JSON
   'APISPEC_SWAGGER_UI_URL': '/swagger-ui'# URI UI of API Doc
})




db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)
ma = Marshmallow(app)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)
# swagger = Swagger(app)
docs = FlaskApiSpec(app)


@app.errorhandler(404)
def not_found(e):
    response = {'status': 404, 'error': e.description}
    return response, 404


@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = db.one_or_404(db.select(UserModel).filter_by(username=username))
    if not user.verify_password(password):
        return False
    return user


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    return user


@basic_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


@token_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


from api.handlers import auth
from api.handlers import note
from api.handlers import user