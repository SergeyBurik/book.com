from django import template

register = template.Library()


@register.filter(name='truncate_text')
def truncate_text(data):
    return (data[:75] + '..') if len(data) > 75 else data
