import mailchimp_transactional as MailChimpTransactional
from app.configs.environments import MAILCHIMP_API_KEY, FROM_EMAIL
from app.configs.logger import logger
from app.utils.validate_fields import validate_fields
from app.interfaces.email_interface import IEmailService


class EmailService(IEmailService):
    _mailchimp_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._mailchimp_instance:
            cls._mailchimp_instance = MailChimpTransactional.Client(
                MAILCHIMP_API_KEY)
        return super().__new__(cls)

    def get_or_create_instance(self):
        return self._mailchimp_instance

    def send_email(self, to_email, b64_pdf):

        validate_fields(target_fields={
            "invoice_pdf": b64_pdf,
            "to_email": to_email,
        }, error_message="missing fields while trying to send the email")

        message = {
            "from_email": FROM_EMAIL,
            "subject": "¡Hola! Esta es tu factura por la transacción de créditos SportClub",
            "text": "En el adjunto encontrarás tu factura en PDF.",
            "to": [{"email": to_email, "type": "to"}],
            "attachments": [
                {
                    "type": "application/pdf",
                    "name": "factura.pdf",
                    "content": b64_pdf,
                }
            ],
        }

        response = self._mailchimp_instance.messages.send({"message": message})
        logger.info(f"Email sended successfully: {response}")
