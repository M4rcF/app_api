from flask_restful import Resource
from models.user import User
from flask_jwt_extended import jwt_required

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