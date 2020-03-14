from django import template
from mainapp.models import Room
import datetime

register = template.Library()


@register.filter(name='query_booking')
def query_booking(elem, day):
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d")

    return eval(f'Room.objects.filter(room__pk={elem.pk}, date="{str(day).split(" ")[0]}")')
