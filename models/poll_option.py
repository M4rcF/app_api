from models.vote import Vote
from sql_alchemy import database

class PollOption(database.Model):
  __tablename__ = 'poll_options'

  id = database.Column(database.Integer, primary_key=True)
  text = database.Column(database.String(50), nullable=False)
  poll_id = database.Column(database.Integer, database.ForeignKey('polls.id'))
  created_at = database.Column(database.DateTime, default=database.func.now(), nullable=False)
  updated_at = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now(), nullable=False)

  votes = database.relationship('Vote', back_populates='poll_option')
  poll = database.relationship('Poll', back_populates='poll_options')

  def __init__(self, text, poll_id):
    self.text = text
    self.poll_id = poll_id

  def to_json(self, current_user):
    voted = False
    vote = Vote.find_by_poll_option_id(self.poll_id, self.id, current_user.id)
    if vote:
      voted = True

    return {
      'id': self.id,
      'text': self.text,
      'votes_count': len(self.votes),
      'voted': voted,
    }
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    [vote.delete() for vote in self.votes]

    database.session.delete(self)
    database.session.commit()

  @classmethod
  def find_by_id(cls, poll_option_id):
    user = cls.query.filter_by(id = poll_option_id).first()
    if user:
      return user
    
    return None