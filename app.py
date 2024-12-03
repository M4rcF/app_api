from flask import Flask, jsonify
from flask_restful import Api
from controllers.polls import PollsController
from controllers.users import UsersController
from controllers.votes import VotesController
from controllers.authentication import SignUpController, LoginController, LogoutController
from flask_jwt_extended import JWTManager
from redis_config import jwt_redis_blocklist, ACCESS_EXPIRES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

api = Api(app)

from sql_alchemy import database
database.init_app(app)

with app.app_context():
    database.create_all()

api.add_resource(SignUpController, '/sign_up')
api.add_resource(LoginController, '/login')
api.add_resource(LogoutController, '/logout')
api.add_resource(UsersController, '/users', '/users/<int:user_id>')
api.add_resource(PollsController, '/polls', '/polls/<int:poll_id>')
api.add_resource(VotesController, '/polls/<int:poll_id>/poll_options/<int:poll_option_id>/votes', '/votes')

if __name__ == '__main__':
    app.run(debug=True)
