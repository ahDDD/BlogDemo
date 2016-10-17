from django import template
register = template.Library()


@register.filter(name='what_tab')
def what_tab(value, argv):
    return ' active' if argv == value else ''