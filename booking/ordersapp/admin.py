from django.contrib import admin
from ordersapp.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = 'id', 'client_email'
