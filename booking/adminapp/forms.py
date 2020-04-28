from django import forms
<<<<<<< Updated upstream
from mainapp.models import Hotel
=======
from mainapp.models import Hotel, Room
>>>>>>> Stashed changes


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
<<<<<<< Updated upstream
        fields = ('name', 'description', 'stars', 'banner', 'is_active')
=======
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
>>>>>>> Stashed changes
