from django import forms

from mainapp.models import Hotel, Room, Facility


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
        return "%s" % obj.name


class HotelFacilityForm(forms.Form):
    CHOICES = (
        ('y', u"yes"),
        ('n', u"no"),
    )
    hotel = NameModelChoiceField(label=u'Hotel', queryset=Hotel.objects.order_by('-name'))  # , initial=Hotel.objects.get(id=1)
    bar = forms.ChoiceField(label=u'<fh', choices=CHOICES)
    pool = forms.ChoiceField(label=u'<fh', choices=CHOICES)
    wifi = forms.ChoiceField(label=u'<fh', choices=CHOICES)
    parking = forms.ChoiceField(label=u'<fh', choices=CHOICES)
    facil = NameModelChoiceField(label=u'Удобства',
                                 queryset=Facility.objects.order_by('-name'), initial=Facility.objects.all())  # get(id=1)


# class HotelFacilityForm(forms.ModelForm):
#
#     class Meta:
#         model = HotelFacility
#         fields = '__all__'
#         # exclude = ()
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # self.fields['facility'].queryset = HotelFacility.get_items().select_related()
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'price', 'description', 'adult', 'kids', 'infants',
                  'is_active')

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }
