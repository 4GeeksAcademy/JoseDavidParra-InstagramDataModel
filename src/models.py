import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String)
    password = Column(String)
    username = Column(String(250), nullable=False)
    posts = relationship('Post',backref='users',lazy=True)
    likes  =relationship('Like',backref='users',lazy=True)
    comments = relationship('Comment',backref='users',lazy=True)
    friends = relationship('Friend',backref='users',lazy=True)
    conversations = relationship('Conversation',backref='users',lazy=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable = False)
    date = Column(DateTime)
    footer = Column(String(600))
    likes = relationship('Like',backref='posts',lazy=True)
    comments = relationship('Comment',backref='comments',lazy=True)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'))
    post_id = Column(Integer,ForeignKey('posts.id'))
    comment = Column(String(400))

class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(Integer,ForeignKey('users.id'),primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id'),primary_key=True)

class Friendship(Base):
    __tablename__ = 'friendships'
    # id = Column(Integer,primary_key=True)
    friend1_id = Column(Integer,ForeignKey('users.id'),primary_key=True)
    friend2_id = Column(Integer,ForeignKey('users.id'),primary_key=True)

class Conversation(Base):
    __tablename__ = 'conversations'
    user1_id = Column(Integer,ForeignKey('users.id'),primary_key=True)
    user2_id = Column(Integer,ForeignKey('users.id'),primary_key=True)
    conv = Column(Text)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
