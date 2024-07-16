from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/emails/", response_model=schemas.Email)
def create_email(email: schemas.EmailCreate, db: Session = Depends(get_db)):
  return crud.create_email(db=db, email=email)

@app.get("/emails/{email_id}", response_model=schemas.Email)
def read_email(email_id: int, db: Session = Depends(get_db)):
  db_email = crud.get_email(db, email_id=email_id)
  if db_email is None:
    raise HTTPException(status_code=404, detail="Email not found")
  return db_email
