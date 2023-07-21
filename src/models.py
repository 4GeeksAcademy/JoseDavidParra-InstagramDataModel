import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Enum
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()
user_conversations = Table('conversations',Base.metadata,
                           Column('conv_id',Integer,primary_key=True),
                           Column('user1_id',Integer,ForeignKey('users.id')),
                           Column('user2_id',Integer,ForeignKey('users.id')),
                           Column('conv',Text))

# user_conversations = Table('conversations',Base.metadata,
#                            Column('user1_id',Integer,ForeignKey('conversation.id'),primary_key=True),
#                            Column('user2_id',Integer,ForeignKey('users.id'),primary_key=True),
#                            Column('conv',Text))

user_followers = Table('followers',Base.metadata,
                      Column('user_from_id',Integer,ForeignKey('follower.id'),primary_key=True),
                      Column('user_to_id',Integer,ForeignKey('users.id'),primary_key=True))

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    posts = relationship('Post',backref='users',lazy=True)
    likes  =relationship('Like',backref='users',lazy=True)
    comments = relationship('Comment',backref='users',lazy=True)
    followers = relationship('Follower',secondary = user_followers,lazy='subquery',
                             backref=backref('users',lazy=True))
    # conversations = relationship('user',secondary=user_conversations,lazy='subquery',
    #                              backref = backref('users',lazy = True))
    Conversations = relationship('User',secondary = user_conversations,
                                 primaryjoin = id == user_conversations.c.user1_id,
                                 secondaryjoin = id == user_conversations.c.user2_id,
                                 backref = backref('users',lazy = True))

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer,primary_key=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable = False)
    date = Column(DateTime)
    footer = Column(String(600))
    likes = relationship('Like',backref='posts',lazy=True)
    comments = relationship('Comment',backref='comments',lazy=True)
    post_media = relationship('Media',backref='post',lazy=True)

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer,primary_key = True)
    type = Column(Enum)
    url = Column(String)
    post_id = Column(Integer,ForeignKey('posts.id'))

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

# class Conversation(Base):
#     __tablename__ = 'conversation'
#     id = Column(Integer,primary_key=True)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
