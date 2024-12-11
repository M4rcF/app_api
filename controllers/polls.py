from flask_restful import Resource, reqparse
from models.poll_option import PollOption
from models.poll import Poll
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

def get_current_user():
  try:
    current_user_email = get_jwt_identity()
    if current_user_email:
      return User.find_by_email(current_user_email)
  except Exception:
    return None

def polls_permitted_params():
  polls_args = reqparse.RequestParser()
  polls_args.add_argument('title', type=str, required=True, help="The field 'title' not can be blank")
  polls_args.add_argument('description', type=str, required=True, help="The field 'description' not can be blank")
  polls_args.add_argument('expires_at', type=str, required=True)
  polls_args.add_argument('poll_options', type=dict, action="append", required=True)

  return polls_args.parse_args()

def format_date(date):
  if date:
    return datetime.strptime(date, '%Y-%m-%d').date()

  return None
class PollsController(Resource):
  @jwt_required()
  def get(self, poll_id=None):
    current_user = get_current_user()

    if poll_id is None:
      polls = Poll.get_all()
      return { 'polls': [poll.to_json(current_user) for poll in polls] }, 200
    
    poll = Poll.find_by_id(poll_id)
    if poll:
      return poll.to_json(current_user), 200
    
    return { 'message': 'Poll not found' }, 400


  @jwt_required()
  def post(self):
    current_user = get_current_user()
    data = polls_permitted_params()

    try:
      poll = Poll(data['title'], data['description'], format_date(data['expires_at']), current_user.id)
      poll.save()
    except Exception as e:
      return { 'message': f'An error ocurred trying to create poll: {str(e)}' }, 500
    
    try:
      for option in data['poll_options']:
        poll_option = PollOption(option['text'], poll.id)
        poll_option.save()
    except Exception as e:
      return { 'message': f'An error ocurred trying to create poll_option: {str(e)}' }, 500
    
    return poll.to_json(current_user), 201
  
  @jwt_required()
  def put(self, poll_id):
    updated_polls_args = polls_permitted_params()
    current_user = get_current_user()

    try:
      poll = Poll.find_by_id(poll_id)

      if current_user and (poll.user_id == current_user.id or current_user.is_admin):
        poll.update(updated_polls_args['title'], updated_polls_args['description'], format_date(updated_polls_args['expires_at']), updated_polls_args['poll_options'])
        return { "message": "Poll updated" }, 200

      return {"message": "Access denied. Only administrators can access."}, 403
    except Exception as e:
      return { 'message': f'An error ocurred trying to update poll: {str(e)}' }, 500

  @jwt_required()
  def delete(self, poll_id):
    poll = Poll.find_by_id(poll_id)
    if poll:
      poll.delete()

      return { 'message': 'Poll deleted' }, 200
    
    return { 'message': 'Poll not found' }, 400