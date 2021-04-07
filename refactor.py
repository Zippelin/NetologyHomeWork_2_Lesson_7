import email
import smtplib
import imaplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailWorker:
    __BASE_URL = "gmail.com"
    __GMAIL_SMTP = '.'.join(('smtp', __BASE_URL))
    __GMAIL_IMAP = '.'.join(('imap', __BASE_URL))
    __SMTP_PORT = 587
    __IMAP_SSL_PORT = 993

    __CONNECTORS = {
        'send': smtplib.SMTP,
        'receive': imaplib.IMAP4_SSL
    }

    def __init__(self, login, password):
        self.__login = login
        self.__password = password

    def process_message(self, method=None, message=None, filter_='ALL'):
        port = self.__IMAP_SSL_PORT
        host = self.__GMAIL_IMAP
        if method == 'send':
            port = self.__SMTP_PORT
            host = self.__GMAIL_SMTP
        with self.__CONNECTORS[method](host=host, port=port) as connector:
            if method == 'send':
                connector.ehlo()
                connector.starttls()
                connector.ehlo()
            try:
                connector.login(self.__login, self.__password)
            except Exception as e:
                print(e)
                return
            if method == 'send':
                connector.sendmail(self.__login, connector, message.as_string())
                return
            connector.list()
            connector.select("inbox")
            _, data = connector.uid('search', None, '(HEADER Subject "%s")' % filter_)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            _, data = connector.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            return email.message_from_string(raw_email)

    def send(self, text, to, subject=None):
        message = MIMEMultipart(From=self.__login, To=to, Subject=subject)
        message.attach(MIMEText(text, _charset='utf-8'))
        self.process_message('send', message=message)

    def receive(self, filter='ALL'):
        self.process_message('receive', filter)


if __name__ == '__main__':
    mail = MailWorker('text', 'text')
    mail.send('hello', 'aa@22.com')