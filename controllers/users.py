from flask_restful import Resource
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

class UsersController(Resource):
  @jwt_required()
  def get(self, user_id=None):
    current_user_email = get_jwt_identity()
    current_user = User.find_by_email(current_user_email)

    if user_id is not None and (user_id == current_user.id or current_user.is_admin):
      user = User.find_by_id(user_id)
      if user:
        return user.to_json(), 200

      return { "message": "User not found" }, 400

    if current_user and current_user.is_admin:
      users = User.get_all()
      return { 'users': [user.to_json() for user in users] }, 200
    
    return {"message": "Access denied. Only administrators can access."}, 403
