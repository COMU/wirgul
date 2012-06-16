import string
from random import choice


def send_email(frm, to, subject, message):
    pass

def generate_url_id(n):
    url_id = ''.join([choice(string.letters + string.digits) for i in range(20)])
    return url_id
