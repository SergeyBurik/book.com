from django import template
from mainapp.models import Bookings
import datetime

register = template.Library()


@register.filter(name='query_booking')
def query_booking(elem, day):
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d")

    return eval(f'Bookings.objects.filter(room__pk={elem.pk}, date="{str(day).split(" ")[0]}")')
    # return Bookings.objects.filter(room__pk={elem.pk}, date="{str(day).split(" ")[0]}")
