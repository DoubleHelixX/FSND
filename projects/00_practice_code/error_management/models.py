import os
import sys
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import json

database_name = "testing"

database_path = "postgresql+psycopg2://{}:{}@{}/{}".format('postgres', '1','localhost:5432', database_name)

db = SQLAlchemy()




'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  #fapp.config["DEBUG"]=True
  db.app = app
  db.init_app(app)
  db.create_all()




'''
set up migration scripts

'''
def migrationConfig(app):
  migrate = Migrate(app, db)
  manager = Manager(app)
  manager.add_command('db', MigrateCommand)
    
    
    
'''
Book

'''
class Book(db.Model):  
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  author = Column(String)
  rating = Column(Integer)

  def __init__(self, title, author, rating):
    self.title = title
    self.author = author
    self.rating = rating

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'author': self.author,
      'rating': self.rating,
    }
