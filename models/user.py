from sql_alchemy import database

class User(database.Model):
  __tablename__ = 'users'

  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String(20), unique=True)
  password = database.Column(database.String(10))

  def __init__(self, name, password):
    self.name = name
    self.password = password
  
  def to_json(self):
    return { 'name': self.name }
  
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
  def find_by_name(cls, user_name):
    user = cls.query.filter_by(name = user_name).first()
    if user:
      return user
    
    return None
  
  def save(self):
    database.session.add(self)
    database.session.commit()

  def delete(self):
    database.session.delete(self)
    database.session.commit()