# coding: utf-8
import random

from django import template

register = template.Library()


@register.filter(name='random_image')
def random_image(l):
    return l[random.randint(0, len(l)-1)]['url']
