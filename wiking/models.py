from django.db import models
from django.contrib.auth.models import User


class ArticleVersion(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    version = models.PositiveIntegerField(blank=False, null=False, default=1)
    author = models.ForeignKey(User, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=255, blank=True, null=False)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'wiking'


class Article(models.Model):
    slug = models.CharField(max_length=255)
    head = models.ForeignKey(ArticleVersion, related_name='article', null=False)
    owner = models.ForeignKey(User, related_name='created_articles', null=False)
    parent = models.ForeignKey('self', related_name='childs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_title(self):
        return self.head.title

    def get_content(self):
        return self.head.content

    def get_revision(self):
        return self.head.version

    def get_author(self):
        return self.head.author

    def __unicode__(self):
        return self.slug

    class Meta:
        app_label = 'wiking'

