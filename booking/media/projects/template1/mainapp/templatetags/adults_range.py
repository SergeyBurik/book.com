# coding: utf-8
from django import template

register = template.Library()

@register.filter(name='adults_range')
def adults_range(el):
    return range(1, el+1)
