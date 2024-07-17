import os
from celery import Celery
from .database import SessionLocal
from . import crud, schemas
import asyncio

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery(
  "worker",
  broker=os.getenv("REDIS_URL"),
  backend=os.getenv("REDIS_URL"),
  broker_connection_retry_on_startup=True  # Add this line
)

# celery_app.conf.task_routes = {
#   "app.worker.send_email": "email-queue"
# }

@celery_app.task
def divide(x, y):
  import time
  time.sleep(5)
  return x / y

@celery_app.task
def send_email(email_data):
  logger.info(f"Received: {email_data}")
  loop = asyncio.get_event_loop()
  loop.run_until_complete(send_email_async(email_data))
  # asyncio.ensure_future(send_email_async(email_data))
  # asyncio.run(send_email_async(email_data))

async def send_email_async(email_data):
  logger.info(f"will send: {email_data}")
  try:
    async with SessionLocal() as db:
      email = schemas.EmailCreate(**email_data)
      await crud.create_email(db=db, email=email) # async version
      # crud.create_email_sync(db=db, email=email)  # Using sync version of CRUD function
      # db.commit()
      logger.info(f"Email created: {email_data}")
  except Exception as e:
    logger.error(f"Failed to send email: {str(e)}")
    raise
