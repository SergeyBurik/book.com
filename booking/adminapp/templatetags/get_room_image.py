from django import template
from mainapp.models import RoomGallery

register = template.Library()


@register.filter(name='get_room_image')
def get_room_image(room):
    try:
        return RoomGallery.objects.filter(room=room, room__hotel=room.hotel)[0].image.url
    except IndexError:
        return ''
