# coding=utf-8
__author__ = 'Gvammer'
from django import forms
from django.http import HttpResponse
from django.template import RequestContext, loader
from PManager.viewsExt.tools import emailMessage
from tracker.settings import FEEDBACK_EMAIL
import datetime

class WhoAreYou(forms.Form):
    name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    skype = forms.CharField(max_length=255, required=False)
    sitename = forms.CharField(max_length=255, required=False)


class Feedback(forms.Form):

    subject = forms.CharField(max_length=255, label='subject',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Ввведите тему'}))
    message = forms.CharField(max_length=1500, label='message',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': u'Введите сообщение',
                                                           'rows': 2}))


def sendFeedback(request):
    form = Feedback(request.POST or None)
    context = {'form': form}

    if 'subject' in request.POST and form.is_valid():
        context['send'] = True
        mes = {
            'fromUser': request.user.first_name + ' ' + request.user.last_name,
            'userEmail': request.user.email,
            'subject': form.cleaned_data['subject'],
            'message': form.cleaned_data['message'],
            'date': datetime.datetime.now()
        }
        sendMes = emailMessage('feedback', mes, 'New feedback')
        sendMes.send([FEEDBACK_EMAIL, 'alwxsin@gmail.com'])  # if error, admin will know and will resend

    c = RequestContext(request, context)
    t = loader.get_template('helpers/feedback.html')
    return HttpResponse(t.render(c))
