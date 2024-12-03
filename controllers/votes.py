from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.vote import Vote
from models.poll_option import PollOption
from models.user import User

class VotesController(Resource):
  def get(self):
    return { 'votes': [vote.to_json() for vote in Vote.get_all()] }, 200

  @jwt_required()
  def post(self, poll_id, poll_option_id):
    current_user_email = get_jwt_identity()
    current_user = User.find_by_email(current_user_email)

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