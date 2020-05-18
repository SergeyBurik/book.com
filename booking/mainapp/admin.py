from django.contrib import admin
from mainapp.models import Hotel, Room, RoomGallery, RoomAgent, Facility,\
    HotelFacility


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(RoomAgent)
class RoomManagerAdmin(admin.ModelAdmin):
    search_fields = 'name',


class HotelFacilityInline(admin.TabularInline):
    model = Facility
    extra = 3


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    search_fields = 'name',
    list_display = 'name', 'icon',


@admin.register(HotelFacility)
class HotelFacilityAdmin(admin.ModelAdmin):
    search_fields = 'hotel',
    list_display = 'hotel', 'facility',


class RoomGalleryInline(admin.TabularInline):
    model = RoomGallery
    extra = 3


@admin.register(RoomGallery)
class RoomGalleryAdmin(admin.ModelAdmin):
    search_fields = 'room',
    list_display = 'room', 'image',


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = RoomGalleryInline,
    search_fields = 'name', 'hotel__name',
    list_display = 'name',
