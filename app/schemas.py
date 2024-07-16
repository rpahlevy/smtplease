from pydantic import BaseModel

class EmailBase(BaseModel):
  sender: str
  receiver: str
  subject: str
  body: str

class EmailCreate(EmailBase):
  pass

class Email(EmailBase):
  id: int

  class Config:
    orm_mode = True
