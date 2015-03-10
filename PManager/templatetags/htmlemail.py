__author__ = 'Tonakai'
from django.template import Library
import re
register = Library()
@register.filter(name='htmlemail')
def htmlemail(value):
    quote_filter = re.compile(r'&gt;&gt; (.+?)(\r\n|\n)', re.IGNORECASE and re.MULTILINE)
    n2br_filter = re.compile(r'\r\n|\n', re.IGNORECASE)
    value = quote_filter.sub(r'<blockquote class="well">\1</blockquote>', value)
    value = n2br_filter.sub('<br/>', value)
    return value
