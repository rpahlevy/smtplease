from pydantic import BaseModel
from datetime import datetime

class EmailBase(BaseModel):
  sender: str
  receiver: str
  subject: str
  body: str

class EmailCreate(EmailBase):
  pass

class Email(EmailBase):
  id: int
  timestamp: datetime
  is_processed: bool

  class Config:
    orm_mode = True

class EmailProcessingResponse(BaseModel):
  message: str
