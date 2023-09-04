import threading
from random import randint

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.authentication.models import VerifyCode
from config.settings import EMAIL_HOST_USER


class SendHtmlEmailAsync(threading.Thread):
    def __init__(self, from_email=None, to=None, subject=None, html_content=None):
        super(SendHtmlEmailAsync, self).__init__()
        self.from_email = from_email
        self.to = to
        self.subject = subject
        self.html_content = html_content
        self.email_type = 'html'

    def run(self) -> None:
        email = EmailMessage(
            subject=self.subject,
            body=self.html_content,
            from_email=self.from_email,
            to=self.to)
        email.content_subtype = self.email_type
        email.send()


def send_verification_token(template_name, subject, user: User) -> None:
    code = randint(100000, 999999)
    VerifyCode(code=code, user=user).save()
    content = render_to_string(template_name, context={'code': code})
    message = SendHtmlEmailAsync(from_email=EMAIL_HOST_USER, to=[user.email, ], subject=subject, html_content=content)
    message.start()
