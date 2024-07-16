from aiosmtpd.controller import Controller
from email.parser import BytesParser
from .worker import send_email
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
