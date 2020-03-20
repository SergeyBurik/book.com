from django import forms
from mainapp.models import Hotel


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'description', 'stars', 'banner', 'is_active')
