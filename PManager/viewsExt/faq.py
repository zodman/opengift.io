__author__ = 'Gvammer'
from django.shortcuts import HttpResponse
from PManager.models import FaqQuestions, FaqQuestionsCategory
from django.template import loader, RequestContext

def list(request):
    cat = FaqQuestionsCategory.objects.order_by('sort')
    a_categories = []
    for category in cat:
        a_categories.append({
            'category': category,
            'questions': FaqQuestions.objects.filter(category=category).order_by('sort')
        })

    c = RequestContext(request, {
            'categories': a_categories,
            'need_inverse': True
        })

    return HttpResponse(loader.get_template('public/faq.html').render(c))