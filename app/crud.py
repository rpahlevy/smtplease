from sqlalchemy.orm import Session
from . import models, schemas

def get_email(db: Session, email_id: int):
  return db.query(models.Email).filter(models.Email.id == email_id).first()

def create_email(db: Session, email: schemas.EmailCreate):
  db_email = models.Email(**email.dict())
  db.add(db_email)
  db.commit()
  db.refresh(db_email)
  return db_email
