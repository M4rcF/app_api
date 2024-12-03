from flask_restful import Api
from controllers.polls import PollsController
from controllers.users import UsersController
from controllers.votes import VotesController
from controllers.authentication import SignUpController, LoginController, LogoutController

def register_routes(app):
    api = Api(app)

    api.add_resource(SignUpController, '/sign_up')
    api.add_resource(LoginController, '/login')
    api.add_resource(LogoutController, '/logout')
    api.add_resource(UsersController, '/users', '/users/<int:user_id>')
    api.add_resource(PollsController, '/polls', '/polls/<int:poll_id>')
    api.add_resource(VotesController, '/polls/<int:poll_id>/poll_options/<int:poll_option_id>/votes', '/votes')
