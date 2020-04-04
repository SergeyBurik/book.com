# coding: utf-8

from django import template

register = template.Library()


@register.filter(name='file_name')
def file_name(file, path):
    file = file.replace(path, '')  # remove path
    file = file.split('.')[0]  # remove file extension
    return file
