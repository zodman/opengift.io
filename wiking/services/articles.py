__author__ = 'rayleigh'
from wiking.models import Article, ArticleVersion
import os


class ArticleService:
    ROOT_PATH = '/wiki'
    PATH_NOT_FIND = 1
    NO_ERRORS = 0

    def __init__(self):
        pass

    @staticmethod
    def get_absolute_url(article, articles=[]):
        return os.path.join(ArticleService.get_parent_path(article, articles), article.slug)

    @staticmethod
    def get_parent_path(article, articles=[]):
        path = ArticleService.ROOT_PATH
        if article.project is not None:
            path = os.path.join(path, 'project')
            path = os.path.join(path, article.project.id)
        for article in articles:
            path = os.path.join(path, article.slug)
        return path

    @staticmethod
    def create_article(data, user):
        version = ArticleService.create_version(data, user)
        article = Article()
        article.parent = data['parent']
        article.slug = data['slug']
        article.owner = user
        article.head = version
        if data['parent']:
            article.level = data['parent'].level + 1
        article.save()
        return article

    @staticmethod
    def update_article(article, data, user):
        new_version = ArticleService.create_version(data, user, article.head.version)
        article.head = new_version
        article.save()
        return article

    @staticmethod
    def create_version(data, user, last_version=0):
        version = ArticleVersion()
        version.title = data['title']
        version.content = data['content']
        version.comment = data['comment']
        version.author = user
        version.version = last_version + 1
        version.save()
        return version

    @staticmethod
    def get_breadcrumbs(articles):
        output = list()
        articles = list(articles)
        while len(articles) > 0:
            article = articles.pop()
            path = ArticleService.get_absolute_url(article, articles)
            output.append({'path': path, 'article': article})
        output.reverse()
        return output

    @staticmethod
    def get_article(parent, slug):
        try:
            article = Article.objects.get(slug=slug, parent=parent)
            return article
        except Article.DoesNotExist:
            return None

    @staticmethod
    def get_form_data(article):
        data = dict()
        data['slug'] = article.slug
        data['comment'] = ''
        data['content'] = article.get_content()
        data['title'] = article.get_title()
        return data

    @staticmethod
    def get_create_path(article_slug, project=None):
        path = ArticleService.ROOT_PATH
        if project is not None:
            path = os.path.join(path, 'project')
            path = os.path.join(path, project.id)
        return os.path.join(path, 'new') + '?slug=' + article_slug

    @staticmethod
    def parse_slug(raw_slug):
        slugs = raw_slug.strip('/').split('/')
        slug = slugs.pop()
        parent = None
        articles = []
        error = ArticleService.NO_ERRORS
        if len(slugs) > 0:
            parent_level = len(slugs) - 1
            parent_slug = slugs[len(slugs) - 1]
            articles = Article.objects.filter(slug__in=slugs).order_by('level')
            if len(slugs) != len(articles):
                error = ArticleService.PATH_NOT_FIND
            for article in articles:
                if article.slug == parent_slug and parent_level == article.level:
                    parent = article
        return parent, slug, articles, error
