from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.vote import Vote
from models.user import User

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None
class VotesController(Resource):
  @jwt_required()
  def get(self):
    current_user = get_current_user()

    if current_user.is_admin:
      return { 'votes': [vote.to_json() for vote in Vote.get_all()] }, 200
    
    return {'message': 'Unauthorized'}, 401

  @jwt_required()
  def post(self, poll_id, poll_option_id):
    current_user = get_current_user()

    try:
      current_vote = Vote.find_by_poll_option_id(poll_id, poll_option_id, current_user.id)

      if current_vote:
        current_vote.delete()
      else:
        vote = Vote.find_by_poll_id(poll_id, current_user.id)

        new_vote = Vote(poll_id, poll_option_id, current_user.id)

        if vote:
          vote.update(poll_option_id)
        else:
          new_vote.save()
    except Exception as e:
      return { 'message': f'An error ocurred trying to vote: {str(e)}' }, 500
    
    return { 'message': 'Success' }, 200