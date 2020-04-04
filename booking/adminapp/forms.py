from django import forms
from mainapp.models import Hotel, Room


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'description', 'stars', 'location', 'banner', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'price', 'description', 'adult', 'kids', 'infants',
                  'is_active')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }
