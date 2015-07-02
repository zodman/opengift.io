# coding=utf-8
__author__ = 'Gvammer'
from django import forms
from django.http import HttpResponse
from django.template import RequestContext, loader
from PManager.viewsExt.tools import emailMessage
from tracker.settings import INFO_EMAIL
import datetime

class WhoAreYou(forms.Form):
    name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    skype = forms.CharField(max_length=255, required=False)
    sitename = forms.CharField(max_length=255, required=False)


class Feedback(forms.Form):

    subject = forms.CharField(max_length=255, required=True, label='subject',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Ввведите имя'}))
    message = forms.CharField(max_length=1500, required=True, label='message',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': u'Введите сообщение',
                                                           'rows': 2}))


def sendFeedback(request):
    form = Feedback(request.POST or None)
    context = {'form': form}
    # print request.POST, form

    if 'subject' in request.POST:
        if form.is_valid():
            # context['send'] = True
            mes = {
                'user': request.user,
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
                'date': datetime.datetime.now()
            }
            # t = loader.get_template('mail_templates/feedback.html')
            # c = RequestContext(request, mes)
            # return HttpResponse(t.render(c))
            sendMes = emailMessage('feedback', mes, 'New feedback', u_from=request.user)
            try:
                sendMes.send(INFO_EMAIL)
            except Exception:
                print 'Message is not sent'

    c = RequestContext(request, context)

    t = loader.get_template('helpers/feedback.html')
    return HttpResponse(t.render(c))
