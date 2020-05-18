# coding: utf-8
import random
from django import template

register = template.Library()

@register.filter(name='range')
def range_(el):
    return range(el)
