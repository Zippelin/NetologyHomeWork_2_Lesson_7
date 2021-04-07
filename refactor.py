import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailWorker:
    __BASE_URL = "gmail.com"
    __GMAIL_SMTP = '.'.join(('smtp', __BASE_URL))
    __GMAIL_IMAP = '.'.join(('imap', __BASE_URL))
    _SMTP_PORT = 587

    def __init__(self, login, password):
        self.__login = login
        self.__password = password

    def send_message(self, text, to, subject=None):
        with smtplib.SMTP(self.__GMAIL_SMTP, self._SMTP_PORT) as smtp_connector:
            message = MIMEMultipart(From=self.__login, To=to, Subject=subject)
            message.attach(MIMEText(text, _charset='utf-8'))

            # identify ourselves to smtp gmail client
            smtp_connector.ehlo()
            # secure our email with tls encryption
            smtp_connector.starttls()
            # re-identify ourselves as an encrypted connection
            smtp_connector.ehlo()

            try:
                smtp_connector.login(self.__login, self.__password)
            except smtplib.SMTPAuthenticationError as e:
                print(e)
                return
            smtp_connector.sendmail(self.__login, smtp_connector, message.as_string())

    def receive_message(self, filter='ALL'):
        with imaplib.IMAP4_SSL(self.__GMAIL_IMAP) as imap_connector:
            try:
                imap_connector.login(self.__login, self.__password)
            except Exception as e:
                print(e)
                return
            imap_connector.list()
            imap_connector.select("inbox")
            _, data = imap_connector.uid('search', None, '(HEADER Subject "%s")' % filter)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            _, data = imap_connector.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            return email.message_from_string(raw_email)


if __name__ == '__main__':
    mail = MailWorker('text', 'text')
    mail.send_message('hello', 'aa@22.com')