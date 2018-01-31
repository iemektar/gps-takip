from django import forms
from .models import IoT
from django.shortcuts import reverse

class IoTForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(IoTForm, self).__init__(*args,**kwargs)
        self.fields['serial_no'].widget.attrs['validation'] = reverse('iot:validate_serial_no')
        self.fields['plate_no'].widget.attrs['validation'] = reverse('iot:validate_plate_no')

        if not self.instance.serial_no == str():
            self.fields['serial_no'].widget.attrs['readonly'] = True

    class Meta:
        model = IoT
        fields = ['serial_no','plate_no']
        labels = {
            'serial_no': 'Seri Numarası',
            'plate_no': 'Plaka Numarası'
        }

        widgets = {
            'serial_no': forms.TextInput(attrs=
                                         {
                                             'class': 'form-control',
                                             'id': 'serial_no',
                                             'validation': ''
                                         }),
            'plate_no': forms.TextInput(attrs=
                                         {
                                             'class': 'form-control',
                                             'id': 'plate_no',
                                             'validation': ''
                                         }),
        }