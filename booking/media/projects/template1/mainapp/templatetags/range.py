# coding: utf-8
from django import template

register = template.Library()

@register.filter(name='range')
def range_(el):
    return range(el)
