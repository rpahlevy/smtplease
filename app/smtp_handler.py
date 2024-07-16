from aiosmtpd.controller import Controller
from email.parser import BytesParser
from .worker import send_email
from .database import SessionLocal
from . import crud
from aiosmtpd.handlers import Debugging

class CustomSMTPHandler(Debugging):
  async def handle_DATA(self, server, session, envelope):
    message = BytesParser().parsebytes(envelope.content)
    email_data = {
        "sender": message["From"],
        "receiver": message["To"],
        "subject": message["Subject"],
        "body": message.get_payload()
    }
    send_email.delay(email_data)
    return '250 Message accepted for delivery'

async def run_smtp_server():
  handler = CustomSMTPHandler()
  server = Controller(handler)
  await server.start()

async def get_emails_from_db(skip: int = 0, limit: int = 10):
  async with SessionLocal() as db:
    emails = await crud.get_emails(db, skip=skip, limit=limit)
    return emails

# TODO. IMAP Server implementation
async def imap_server(reader, writer):
  writer.write(b'* OK IMAP4rev1 Service Ready\r\n')
  await writer.drain()

  while True:
    data = await reader.readline()
    if not data:
      break

    command = data.decode().strip().split()
    if command[0].lower() == 'login':
      writer.write(b'* OK LOGIN completed\r\n')
    elif command[0].lower() == 'select':
      emails = await get_emails_from_db()
      writer.write(f'* {len(emails)} EXISTS\r\n'.encode())
      writer.write(b'* OK [READ-WRITE] SELECT completed\r\n')
    elif command[0].lower() == 'fetch':
      emails = await get_emails_from_db()
      for i, email in enumerate(emails):
          message = f'* {i+1} FETCH (BODY[HEADER] {{{len(email.body)}}}\r\n{email.body}\r\n'
          writer.write(message.encode())
      writer.write(b'OK FETCH completed\r\n')
    elif command[0].lower() == 'logout':
      writer.write(b'* BYE IMAP4rev1 Server logging out\r\n')
      writer.write(b'OK LOGOUT completed\r\n')
      break
    else:
      writer.write(b'BAD Command not recognized\r\n')

    await writer.drain()

  writer.close()
  await writer.wait_closed()