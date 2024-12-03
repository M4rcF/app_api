from flask_restful import Resource, reqparse
from models.vote import Vote
from models.poll_option import PollOption
from models.poll import Poll
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

def polls_permitted_params():
  polls_args = reqparse.RequestParser()
  polls_args.add_argument('title', type=str, required=True, help="The field 'title' not can be blank")
  polls_args.add_argument('description', type=str, required=True, help="The field 'description' not can be blank")
  polls_args.add_argument('expires_at', type=str, required=True, help="The field 'expires_at' not can be blank")
  polls_args.add_argument('poll_options', type=dict, action="append")

  return polls_args.parse_args()

def get_current_user():
  current_user_email = get_jwt_identity()
  return User.find_by_email(current_user_email)

class PollsController(Resource):
  @jwt_required()
  def get(self, poll_id=None):
    if poll_id is None:
      polls = Poll.get_all()
      return { 'polls': [poll.to_json() for poll in polls] }, 200
    
    poll = Poll.find_by_id(poll_id)

    return poll.to_json(), 200

  @jwt_required()
  def post(self):
    current_user = get_current_user()
    data = polls_permitted_params()

    try:
      formatted_date = datetime.strptime(data['expires_at'], '%Y-%m-%dT%H:%M:%S')
      poll = Poll(data['title'], data['description'], formatted_date, current_user.id)
      poll.save()
    except Exception as e:
      return { 'message': f'An error ocurred trying to create poll: {str(e)}' }, 500
    
    try:
      for option in data['poll_options']:
        poll_option = PollOption(option['text'], poll.id)
        poll_option.save()
    except Exception as e:
      return { 'message': f'An error ocurred trying to create poll_option: {str(e)}' }, 500
    
    return poll.to_json(), 201
  
  @jwt_required()
  def put(self, poll_id):
    updated_polls_args = reqparse.RequestParser()
    updated_polls_args.add_argument('title', type=str, required=True, help="The field 'title' not can be blank")
    updated_polls_args.add_argument('description', type=str, required=True, help="The field 'description' not can be blank")
    current_user = get_current_user()

    try:
      poll = Poll.find_by_id(poll_id)

      if current_user and (poll.user_id == current_user.id or current_user.is_admin):
        poll.update(**updated_polls_args.parse_args())
        return { "message": "Poll updated" }, 200

      return {"message": "Access denied. Only administrators can access."}, 403
    except:
      return { 'message': f'An error ocurred trying to update poll: {str(e)}' }, 500

  @jwt_required()
  def delete(self, poll_id):
    poll = Poll.find_by_id(poll_id)
    if poll:
      poll.delete()

      return { 'message': 'Poll deleted' }, 200
    
    return { 'message': 'Poll not found' }, 400