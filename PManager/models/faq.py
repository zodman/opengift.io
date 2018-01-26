__author__ = 'Gvammer'
from django.db import models

class FaqQuestionsCategory(models.Model):
    name = models.CharField(max_length=500)
    sort = models.IntegerField(default=100)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'PManager'

class FaqQuestions(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    question = models.CharField(max_length=500)
    answer = models.TextField(max_length=2000)
    category = models.ForeignKey(FaqQuestionsCategory, related_name='questions')
    sort = models.IntegerField(default=100)

    def __unicode__(self):
        return self.question

    class Meta:
        app_label = 'PManager'