# from flask_restful import Resource, reqparse
# from models.user import UserModel

# users = [
#   {
#     'id': '1',
#     'name': 'Admin',
#     'email': 'admin@admin.com'
#   },
#   {
#     'id': '2',
#     'name': 'Ana',
#     'email': 'ana@hotmail.com'
#   }
# ]

# class Users(Resource):
#   def get(self):
#     return { 'users': users }

# class User(Resource):
  # permitted_args = reqparse.RequestParser()
  # permitted_args.add_argument('name')
  # permitted_args.add_argument('email')

  # def find_user(user_id):
  #   for user in users:
  #     if user['id'] == user_id:
  #       return user
  #   return None

  # def get(self, user_id):
  #   user = User.find_user(user_id)

  #   if user:
  #     return user
  #   return { 'message': 'User not found' }, 400

  # def post(self, user_id):
  #   data = User.permitted_args.parse_args()
  #   new_user = UserModel(user_id, **data).to_json()

  #   users.append(new_user)

  #   return new_user, 200

  # def put(self, user_id):
  #   user = User.find_user(user_id)
  #   data = User.permitted_args.parse_args()
  #   new_user = UserModel(user_id, **data).to_json()

  #   if user:
  #     user.update(new_user)

  #     return user, 200
    
  #   users.append(new_user)
  #   return new_user, 201

  # def delete(self, user_id):
  #   global users

  #   users = [user for user in users if user['id'] != user_id]
  #   return { 'message': 'User deleted' }, 200