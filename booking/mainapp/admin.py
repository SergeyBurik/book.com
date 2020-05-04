from django.contrib import admin
from mainapp.models import Hotel, Room, RoomGallery, RoomAgent, HotelComfort


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    search_fields = 'name',


class HotelComfortInline(admin.TabularInline):
    model = HotelComfort


@admin.register(HotelComfort)
class HotelComfortAdmin(admin.ModelAdmin):
    list_display = 'hotel',


@admin.register(RoomAgent)
class RoomManagerAdmin(admin.ModelAdmin):
    search_fields = 'name',


class RoomGalleryInline(admin.TabularInline):
    model = RoomGallery
    extra = 3


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = RoomGalleryInline,
    search_fields = 'name', 'hotel__name',
    list_display = 'name',


@admin.register(RoomGallery)
class RoomGalleryAdmin(admin.ModelAdmin):
    search_fields = 'room',
    list_display = 'room', 'image',
