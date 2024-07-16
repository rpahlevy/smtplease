from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas
from .database import SessionLocal, engine
from .worker import send_email
# import threading

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Dependency
async def get_db():
  async with SessionLocal() as db:
    yield db

@app.post("/emails/", response_model=schemas.EmailProcessingResponse)
async def create_email(email: schemas.EmailCreate):
  try:
    # without worker
    # await crud.create_email(db=db, email=email)
    # with worker
    logger.info(f"Queuing email task: {email.dict()}")
    send_email.delay(email.dict())
    return {"message": "Email is being processed"}
  except Exception as e:
    logger.error(f"Failed to send email: {str(e)}")
    raise

@app.get("/emails/", response_model=List[schemas.Email])
async def read_emails(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
  emails = await crud.get_emails(db, skip=skip, limit=limit)
  return emails

@app.get("/emails/{email_id}", response_model=schemas.Email)
async def read_email(email_id: int, db: AsyncSession = Depends(get_db)):
  db_email = await crud.get_email(db, email_id=email_id)
  if db_email is None:
    raise HTTPException(status_code=404, detail="Email not found")
  return db_email

# Start SMTP server in a separate thread
# smtp_thread = threading.Thread(target=run_smtp_server)
# smtp_thread.start()