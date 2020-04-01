from django import template
from mainapp.models import Bookings
import datetime


class FixTravis(Bookings):
    pass


register = template.Library()


@register.filter(name='query_booking')
def query_booking(elem, day):
    day = datetime.datetime.strptime(str(day), "%Y-%m-%d")
    # res = eval(f'Bookings.objects.filter(room__pk={elem.pk},'
    #            f' date="{str(day).split(" ")[0]}")')
    # return res
    return eval(f'Bookings.objects.filter(room__pk={elem.pk}, date="{str(day).split(" ")[0]}")')
    # return Bookings.objects.filter(room__pk={elem.pk}, date="{str(day).split(" ")[0]}")
