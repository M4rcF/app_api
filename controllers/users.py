from flask_restful import Resource, reqparse
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac
from redis_config import jwt_redis_blocklist, ACCESS_EXPIRES

permitted_args = reqparse.RequestParser()

permitted_args.add_argument('name', type=str, required=True, help="The field 'login' not can be blank")
permitted_args.add_argument('password', type=str, required=True, help="The field 'password' not can be blank")

class UsersController(Resource):
  @jwt_required()
  def get(self):
    users = User.get_all()

    formatted_users = [user.to_json() for user in users]
    return { 'users': formatted_users }

class UserController(Resource):
  def get(self, user_id):
    user = User.find_by_id(user_id)
    if user:
      return user.to_json(), 200
    
    return { 'message': 'User not found' }, 400

  def post(self, user_id):
    pass

  def put(self, user_id):
    pass

  def delete(self, user_id):
    user = User.find_by_id(user_id)
    if user:
      user.delete()

      return { 'message': 'User deleted' }, 200
    
    return { 'message': 'User not found' }, 400
  
class UserSignUpController(Resource):
  def post(self):
    data = permitted_args.parse_args()

    user = User(**data)
    user.save()

    return { 'message': 'User created' }, 201
  
class UserLoginController(Resource):
  def post(self):
    data = permitted_args.parse_args()
    user = User.find_by_name(data['name'])

    if user and hmac.compare_digest(user.password, data['password']):
      token = create_access_token(identity=user.name)
      return { 'token': token }, 201
    
    return { 'message': 'name or password incorrect' }, 401
  
class UserLogoutController(Resource):
  @jwt_required()
  def post(self):
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return { 'message': 'Logged out successfully' }, 200