__author__ = 'Gvammer'
from django.core.mail import EmailMessage, BadHeaderError

class PM_MailEvent:
    from_address = 'info@tracker.ru'
    to = ['']
    subject = ''
    message = ''

    event_name = ''
    @staticmethod
    def validateEmail(email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def send(self):
        if self.validateEmail(self.to):
            try:
                msg = EmailMessage(self.subject, self.message, self.from_address, [self.to])
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                #send_mail(self.subject, self.message, self.from_address,self.to, fail_silently=True)
            except BadHeaderError:
                return 'Invalid header found.'

        return True
