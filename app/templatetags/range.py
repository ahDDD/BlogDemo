from django import template
register = template.Library()

@register.filter(name='range')
def range(value, page_num):
    '''
    if you want to replace the ','  I'm sorry, I can't help you
    '''
    if page_num - 3 < 0:
        lists = list(value)[:5]
    elif page_num + 2 > len(value):
        lists = list(value)[-5:]
    else:
        lists = list(value)[page_num-3:page_num+2]
    return lists