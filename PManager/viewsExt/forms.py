__author__ = 'Gvammer'
from django import forms

class WhoAreYou(forms.Form):
    name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    skype = forms.CharField(max_length=255, required=False)
    sitename = forms.CharField(max_length=255, required=False)