from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    tokens = relationship('Token', back_populates='user')
    additional_info = relationship('AdditionalInfo', uselist=False, back_populates='user')


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    
    user = relationship('User', back_populates='tokens')

class AdditionalInfo(Base):
    __tablename__ = 'additional_info'

    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    user = relationship('User', back_populates='additional_info')

