import email
import smtplib
import imaplib
from email.message import Message

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


class EmailClient:
    def __init__(
        self, smtp_server: str, imap_server: str, login: str, password: str
    ) -> None:
        """Initialize the EmailClient with SMTP and IMAP server details, login and password."""
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.login = login
        self.password = password

    def send_email(self, recipients: List[str], subject: str, message: str) -> None:
        """Send an email to the specified recipients."""
        msg = MIMEMultipart()
        msg["From"] = self.login
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(message))

        with smtplib.SMTP(self.smtp_server, 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.login, self.password)
            smtp.sendmail(self.login, recipients, msg.as_string())

    def receive_email(self, header=None) -> email.message.Message:
        """Receive the latest email matching the specified header or all emails if no header is provided."""
        with imaplib.IMAP4_SSL(self.imap_server) as mail:
            mail.login(self.login, self.password)
            mail.list()
            mail.select("inbox")
            criterion = '(HEADER Subject "%s")' % header if header else "ALL"
            result, data = mail.uid("search", None, criterion)
            if not data[0]:
                raise ValueError("There are no letters with the specified header")
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid("fetch", latest_email_uid, "(RFC822)")
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email)
        return email_message


if __name__ == "__main__":
    GMAIL_SMTP = "smtp.gmail.com"
    GMAIL_IMAP = "imap.gmail.com"
    EMAIL = "login@gmail.com"
    PASSWORD = "qwerty"
    email_client = EmailClient(GMAIL_SMTP, GMAIL_IMAP, EMAIL, PASSWORD)

    # Send an email
    recipients = ["vasya@email.com", "petya@email.com"]
    subject = "Subject"
    message = "Message"
    email_client.send_email(recipients, subject, message)

    # Receive an email
    try:
        email_message = email_client.receive_email(header="Subject")
        print(email_message)
    except ValueError as err:
        print(err)