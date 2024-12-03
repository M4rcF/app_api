from sql_alchemy import database

class User(database.Model):
  __tablename__ = 'users'

  id = database.Column(database.Integer, primary_key=True)
  email = database.Column(database.String(20), unique=True, nullable=False)
  password = database.Column(database.String(10), nullable=False)
  individual_id = database.Column(database.Integer, database.ForeignKey('individuals.id'))
  is_admin =database.Column(database.Boolean, default=False)

  individual = database.relationship('Individual', back_populates='user')
  votes = database.relationship('Vote', back_populates='user')
  polls = database.relationship('Poll', back_populates='user')

  def __init__(self, email, password, is_admin, individual_id):
    self.email = email
    self.password = password
    self.is_admin = is_admin
    self.individual_id = individual_id
  
  def to_json(self):
    return {
      'id': self.id,
      'email': self.email,
      'is_admin': self.is_admin,
      'individual': self.individual.to_json()
    }
  
  @classmethod
  def get_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_id(cls, user_id):
    user = cls.query.filter_by(id = user_id).first()
    if user:
      return user
    
    return None

  @classmethod
  def find_by_email(cls, user_email):
    user = cls.query.filter_by(email = user_email).first()
    if user:
      return user
    
    return None
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()