from models.poll_option import PollOption
from sql_alchemy import database

class Poll(database.Model):
  __tablename__ = 'polls'

  id = database.Column(database.Integer, primary_key=True)
  title = database.Column(database.String(50), nullable=False)
  description = database.Column(database.String(100), nullable=False)
  user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
  created_at = database.Column(database.DateTime, default=database.func.now(), nullable=False)
  updated_at = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now(), nullable=False)
  expires_at = database.Column(database.Date, nullable=True)

  user = database.relationship('User', back_populates='polls')
  votes = database.relationship('Vote', back_populates='poll')
  poll_options = database.relationship('PollOption', back_populates='poll')

  def __init__(self, title, description, expires_at, user_id):
    self.title = title
    self.description = description
    self.expires_at = expires_at
    self.user_id = user_id

  def to_json(self, current_user=None):
    expires_date = None
    if self.expires_at:
      expires_date = self.expires_at.strftime('%Y-%m-%d')

    return {
      'id': self.id,
      'title': self.title,
      'description': self.description,
      'individual_name': self.user.to_json()['individual']['name'],
      'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
      'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
      'expires_at': expires_date,
      'poll_options': [poll_option.to_json(current_user) for poll_option in self.poll_options],
      'is_poll_creator': getattr(current_user, 'id', None) == self.user.id,
      'is_blocked': current_user == None
    }
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def update(self, title, description, expires_at, poll_options):
    self.title = title
    self.description = description
    self.expires_at = expires_at

    [poll_option.delete() for poll_option in self.poll_options]
    [PollOption(poll_option['text'], self.id).save() for poll_option in poll_options]

    database.session.add(self)
    database.session.commit()

  def delete(self):
    for poll_option in self.poll_options:
      [vote.delete() for vote in poll_option.votes]

      poll_option.delete()

    database.session.delete(self)
    database.session.commit()

  @classmethod
  def find_by_id(cls, poll_id):
    user = cls.query.filter_by(id = poll_id).first()
    if user:
      return user
    
    return None

  @classmethod
  def get_all(cls):
    return cls.query.all()