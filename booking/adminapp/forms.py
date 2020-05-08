from django import forms

from mainapp.models import Hotel, Room, HotelFacility, Facility


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('name', 'description', 'stars', 'location', 'banner', 'is_active',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }


class FacilityForm(forms.ModelForm):

    class Meta:
        model = Facility
        fields = '__all__'
        # exclude = ()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['facility'].queryset = Facility.get_items().select_related()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%obj.name


class HotelFacilityForm(forms.ModelForm):
    CHOICES = (
        ('y', "yes"),
        ('n', "no"),
    )
    hotel = NameModelChoiceField(label=u'Hotel', queryset=Hotel.objects.order_by('-name'), initial=Hotel.objects.get(id=1))  #
    bar = forms.ChoiceField(label='Bar', choices=CHOICES)
    pool = forms.ChoiceField(label='Swimming pool', choices=CHOICES)
    wifi = forms.ChoiceField(label='Free Wi-Fi', choices=CHOICES)
    parking = forms.ChoiceField(label='Free Parking', choices=CHOICES)

    class Meta:
        model = HotelFacility
        # fields = '__all__'
        exclude = ()
            # ('hotel', 'bar', 'pool', 'credit_card', 'phone_number', 'country',
            #       'company_name', 'is_sending')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name:
                self.fields[field_name].label = ''
                self.fields[field_name].widget.attrs.update(
                    {'class': 'registration-form-input'})

        self.fields['hotel'].widget.attrs.update(
            {
                'type': 'text',
                'placeholder': 'Enter hotel name'

            }
        )
        self.fields['bar'].widget.attrs.update(
            {
                'type': 'text',
                'placeholder': 'Bar'
            }
        )

        self.fields['pool'].widget.attrs.update(
            {
                'type': 'text',
                'placeholder': 'Card Number'
            }
        )

        self.fields['wifi'].widget.attrs.update(
            {
                'type': 'checkbox',
                'placeholder': 'Wifi'
            }
        )

        self.fields['parking'].widget.attrs.update(
            {
                'type': 'checkbox',
                'placeholder': 'parking'
            }
        )

        # self.fields['is_sending'].widget.attrs.update(
        #     {
        #         'type': 'checkbox',
        #         'class': 'sending_checkbox'
        #     }
        # )

    def save(self, commit=True):
        # Сохранение пароля в хешированном формате.
        hotel = super().save(commit=False)
        if commit:
            hotel.save()

        print(hotel)

        return hotel


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'price', 'description', 'adult', 'kids', 'infants',
                  'is_active')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }
