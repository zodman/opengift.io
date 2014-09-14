__author__ = 'Gvammer'
# from haystack import indexes
# from PManager.models import PM_Task
# from django.contrib.auth.models import User
#
# class TaskIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     title = indexes.CharField(model_attr='name')
#     url = indexes.CharField(model_attr='url')
#     pub_date = indexes.DateTimeField(model_attr='dateCreate')
#
#     def get_model(self):
#         return PM_Task
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()
#
# class UserIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     title = indexes.CharField(use_template=True)
#     url = indexes.CharField(use_template=True)
#     pub_date = indexes.DateTimeField(model_attr='date_joined')
#
#     def get_model(self):
#         return User
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()