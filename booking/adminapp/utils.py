# coding:utf-8

# returns correct address
from geopy.geocoders import Nominatim


def get_address(address):
    geolocator = Nominatim(user_agent="get_address")
    location = geolocator.geocode(address)
    return location.address
