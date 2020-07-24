from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import    func ,  TIMESTAMP , and_ ,  ForeignKey, create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship , backref

db = SQLAlchemy()

class Channels(db.Model):
      __tablename__ = "channels"
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String, unique=True ,nullable=False)
      desc = db.Column(db.String, nullable=False)
      time = db.Column(db.String, nullable=False)
      user = db.Column(db.String, nullable=False)
      users = db.relationship('Users',secondary = 'sec',backref='channels',lazy=True)
      messages = db.relationship('Messages',backref='channel',lazy=True)


class Users(db.Model):
      __tablename__ = "users"
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(20), nullable=False)
      email = db.Column(db.String, unique=True, nullable=False)
      messages = db.relationship('Messages',backref='user',lazy=True,cascade='all,delete')
    


class Sec(db.Model):
      __tablename__ = "sec"
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey("users.id") ,nullable=False)
      channel_id = db.Column(db.Integer, db.ForeignKey("channels.id") ,nullable=False)

      
class Messages(db.Model):
      __tablename__ = "messages"
      id = db.Column(db.Integer, primary_key=True)
      message = db.Column(db.String, nullable=False)
      time = db.Column(db.String,nullable=False)
      channel_id = db.Column(db.Integer,db.ForeignKey('channels.id'),nullable=False)
      user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

