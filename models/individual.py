from sql_alchemy import database

class Individual(database.Model):
  __tablename__ = 'individuals'

  id = database.Column(database.Integer, primary_key=True)
  name = database.Column(database.String(30), nullable=False)
  cpf = database.Column(database.String(11), unique=True, nullable=False)
  cellphone = database.Column(database.String(13))

  user = database.relationship('User', back_populates='individual', uselist=False)

  def __init__(self, name, cpf, cellphone):
    self.name = name
    self.cpf = cpf
    self.cellphone = cellphone

  def to_json(self):
    return {
      'id': self.id,
      'name': self.name,
      'cpf': self.cpf,
      'cellphone': self.cellphone
    }
  
  def update(self, name, cpf, cellphone):
    self.name = name
    self.cpf = cpf
    self.cellphone = cellphone

    database.session.add(self)
    database.session.commit()

  def save(self):
    database.session.add(self)
    database.session.commit()