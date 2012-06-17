#! -*- coding: utf-8 -*-
from django.conf import settings
import string
from random import choice
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(SUBJECT, BODY, TO, FROM):
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://www.mysite.com">online</a>!"""

    HTML_BODY = MIMEText(BODY, 'html')
    MESSAGE.attach(HTML_BODY)

    #server = smtplib.SMTP('smtp.gmail.com:587')
    server = smtplib.SMTP(":".join([settings.SMTP_MAIL_SERVER, str(settings.SMTP_PORT)]))

    if __name__ == "__main__":
        server.set_debuglevel(1)

    password = "parola"

    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

def generate_url_id(n):
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id
