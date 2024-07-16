from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
import datetime

Base = declarative_base()

class Email(Base):
  __tablename__ = 'emails'

  id = Column(Integer, primary_key=True, index=True)
  sender = Column(String, index=True)
  receiver = Column(String, index=True)
  subject = Column(String, index=True)
  body = Column(Text)
  timestamp = Column(DateTime, default=datetime.datetime.utcnow)
  is_processed = Column(Boolean, default=False)
