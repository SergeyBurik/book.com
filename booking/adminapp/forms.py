from django import forms

from mainapp.models import Hotel, Room, HotelComfort


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'description', 'stars', 'location', 'banner', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class HotelComfortsForm(forms.ModelForm):
    class Meta:
        model = HotelComfort
        # fields = ('swimming_pool', 'spa', 'wifi',
        #           'shuttle', 'fitness', 'parking', 'bar', 'breakfast', 'beach',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'edit-form-input'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'price', 'description', 'adult', 'kids', 'infants',
                  'is_active')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


if __name__ == '__main__':
    hotel = Hotel.objects.get(pk=1)
    formset = HotelFormSet(instance=hotel)