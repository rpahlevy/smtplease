import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
  DATABASE_URL,
  echo=True,
  # pool_size=20,
  # max_overflow=10,
)
SessionLocal = sessionmaker(
  # autocommit=False,
  # autoflush=False,
  bind=engine,
  class_=AsyncSession
)

Base = declarative_base()
