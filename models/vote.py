from sql_alchemy import database

class Vote(database.Model):
  __tablename__ = 'votes'

  id = database.Column(database.Integer, primary_key=True)
  poll_id = database.Column(database.Integer, database.ForeignKey('polls.id'))
  poll_option_id = database.Column(database.Integer, database.ForeignKey('poll_options.id'))
  user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
  created_at = database.Column(database.DateTime, default=database.func.now(), nullable=False)

  user = database.relationship('User', back_populates='votes')
  poll= database.relationship('Poll', back_populates='votes')
  poll_option = database.relationship('PollOption', back_populates='votes')

  def __init__(self, poll_id, poll_option_id, user_id):
    self.poll_id = poll_id
    self.poll_option_id = poll_option_id
    self.user_id = user_id

  def to_json(self):
    return {
      'id': self.id,
      'individual_name': self.user.individual.name,
      'poll': self.poll.title,
      'poll_option': self.poll_option.text
    }

  def save(self):
    database.session.add(self)
    database.session.commit()

  def update(self, poll_option_id):
    self.poll_option_id = poll_option_id
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()

  @classmethod
  def get_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_poll_id(cls, poll_id, current_user_id):
    vote = cls.query.filter_by(poll_id=poll_id, user_id=current_user_id).first()
    if vote:
      return vote
    
    return None
  
  @classmethod
  def find_by_poll_option_id(cls, poll_id, poll_option_id, current_user_id):
    vote = cls.query.filter_by(poll_id=poll_id, poll_option_id=poll_option_id, user_id=current_user_id).first()
    if vote:
      return vote
    
    return None