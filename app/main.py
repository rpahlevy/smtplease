from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
async def get_db():
  async with SessionLocal() as db:
    yield db

@app.post("/emails/", response_model=schemas.Email)
async def create_email(email: schemas.EmailCreate, db: AsyncSession = Depends(get_db)):
  return await crud.create_email(db=db, email=email)

@app.get("/emails/{email_id}", response_model=schemas.Email)
async def read_email(email_id: int, db: AsyncSession = Depends(get_db)):
  db_email = await crud.get_email(db, email_id=email_id)
  if db_email is None:
    raise HTTPException(status_code=404, detail="Email not found")
  return db_email
