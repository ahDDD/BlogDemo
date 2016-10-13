from django import template
from app.models import Article

register = template.Library()

tag = [v['tag'] for v in Article.objects.values('tag').distinct().all()]

@register.filter(name='yesno_tag')
def yesno_tag(value, yes):
    '''
    I only can pick the values which it key is 'tag'.
    '''
    for i in tag:
        if i in value:
            return yes
    return ''
    # value = str(value).split('/')[3]
    # return yes if value in tag else ''
