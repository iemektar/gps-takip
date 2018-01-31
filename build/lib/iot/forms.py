from django import forms

class CreateIoTForm(forms.Form):
    serial_no = forms.CharField(label='Seri Numarası', widget=forms.TextInput(
                                                        attrs={
                                                            'id': 'serial_no',
                                                            'class': 'form-control',
                                                            'validation': 'validate-serial-no'
                                                        }))

    plate_no = forms.CharField(label='Plaka Numarası', widget=forms.TextInput(
                                                        attrs={
                                                            'id': 'plate_no',
                                                            'class': 'form-control',
                                                            'validation': 'validate-plate-no'
                                                        }))