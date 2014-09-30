__author__ = 'Gvammer'
import datetime
from tracker import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from django.utils import timezone

class emailMessage:
    templateName = ''
    context = None
    subject = ''
    u_from = 'no-reply@heliard.ru'

    def __init__(self, templateName, context, subject, u_from=''):
        setattr(self, 'templateName', templateName)
        setattr(self, 'context', context)
        setattr(self, 'subject', subject)
        if u_from:
            setattr(self, 'u_from', u_from)

    @staticmethod
    def validateEmail(email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def send(self, to):
        t = loader.get_template('mail_templates/' + self.templateName + '.html')
        c = Context(self.context)
        html_content = t.render(c)
        msg = EmailMultiAlternatives(self.subject, '', self.u_from, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

class templateTools:
    class dateTime:
        dateFormat = '%d.%m.%Y %H:%M'
        dateDBFormat = '%Y-%m-%d %H:%M:%S'

        @staticmethod
        def convertToSite(date,format = None):
            if not format: format = '%d.%m.%Y %H:%M'
            if isinstance(date, datetime.datetime):
                date = timezone.localtime(date)
                return date.strftime(format)

        @staticmethod
        def convertToDateTime(date):
            try:
                return datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
            except ValueError:
                try:
                    return datetime.datetime.strptime(date, '%d.%m.%Y')
                except ValueError:
                    return None

        @staticmethod
        def convertFromDb(date):
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')


        @staticmethod
        def timeFromTimestamp(seconds):
            if not seconds: seconds = 0
            return {
                'hours': int(seconds // 3600),
                'minutes': int(seconds % 3600 // 60),
                'seconds': int(seconds%60),
            }

    def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        """
          Returns a random string of length characters from the set of a-z, A-Z, 0-9
          for use as a salt.

          The default length of 12 with the a-z, A-Z, 0-9 character set returns
          a 71-bit salt. log_2((26+26+10)^12) =~ 71 bits
          """
        import random
        try:
            random = random.SystemRandom()
        except NotImplementedError:
            pass
        return ''.join([random.choice(allowed_chars) for i in range(length)])

    @staticmethod
    def getDefaultTaskTemplate():
        with file(settings.project_root + 'tracker/templates/item_templates/task/task.html') as f:
            template = f.read()
        return template

    @staticmethod
    def getMessageTemplates():
        templateFiles = {
            'template': 'task_comment.html',
            'task_close': 'log_message_task_close.html',
            'task_create': 'log_message_task_create.html',
            'status_ready': 'log_message_task_status_ready.html',
            'status_revision': 'log_message_task_status_revision.html',
            'new_responsible': 'log_message_new_responsible.html',
            'critically_up': 'log_message_task_critically_up.html',
            'critically_down': 'log_message_task_close.html',
            'set_plan_time': 'log_message_task_set_plan_time.html',
            'confirm_estimation': 'log_message_task_status_revision.html',
            'task_open': 'log_message_task_critically_up.html'
        }
        templates = {}

        for (c, f) in templateFiles.iteritems():
            with file(settings.project_root + 'tracker/templates/item_templates/messages/'+f) as f:
                templates[c] = f.read()

        return templates

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

class taskExtensions:
    @staticmethod
    def getFileList(queryset):
        from PManager.templatetags.thumbnail import thumbnail
        return [{
                    'name': file.name,
                    'url': str(file),
                    'viewUrl': '/docx/?f=' + str(file.id) if file.type == 'docx' else '',
                    'type': file.type,
                    'thumb100pxUrl': thumbnail(str(file), '100x100') if file.isPicture else '',
                    'is_picture': file.isPicture,
                    'date_create': templateTools.dateTime.convertToSite(file.date_create)
                } for file in queryset]

class TextFilters:
    @staticmethod
    def escapeText(text):
        text = text.replace('"', "'")
        text = text.replace('<script', '<sc ript')
        return text

    @staticmethod
    def getFormattedText(text):
        import re
        from django.template.defaultfilters import linebreaksbr
        text = re.sub(r'(http|www\.)([^\ ^\,\r\n\"]+)',
                      r'<a target="_blank" href="\1\2">\1\2</a>', text)
        text = TextFilters.escapeText(text)
        text = linebreaksbr(text)

        return text