from django import forms

from mainapp.models import Hotel, Room, HotelFacility, Facility


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'description', 'stars', 'location', 'banner', 'is_active',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class HotelFacilityForm(forms.ModelForm):

    class Meta:
        model = HotelFacility
        fields = '__all__'
        # exclude = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['facility'].queryset = Facility.get_items().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'price', 'description', 'adult', 'kids', 'infants',
                  'is_active')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }
