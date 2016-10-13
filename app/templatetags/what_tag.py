from django import template
register = template.Library()


@register.filter(name='what_tag')
def what_tag(value):
    '''
    I only can pick the values which it key is 'tag'.
    '''
    return str(value).split('/')[2]