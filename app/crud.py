from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_email(db: AsyncSession, email: schemas.EmailCreate):
  db_email = models.Email(**email.dict())
  db.add(db_email)
  await db.commit()
  await db.refresh(db_email)
  return db_email

def create_email_sync(db: Session, email: schemas.EmailCreate):
    db_email = models.Email(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

async def get_emails(db: AsyncSession, skip: int = 0, limit: int = 100):
  # return await db.execute(models.Email).offset(skip).limit(limit).all()
  stmt = select(models.Email).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def get_email(db: AsyncSession, email_id: int):
  # return await db.execute(models.Email).filter(models.Email.id == email_id).first()
  stmt = select(models.Email).where(models.Email.id == email_id)
  result = await db.execute(stmt)
  return result.scalars().first()
