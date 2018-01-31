from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.conf.urls import url
from django import forms
from users.models import User
from django.utils.safestring import mark_safe

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı", max_length=15,
                               widget=forms.TextInput(attrs=
                                                      {
                                                          'class': 'form-control',
                                                          'id': 'username'
                                                      }))
    password = forms.CharField(label="Şifre", max_length=30,
                               widget=forms.TextInput(attrs=
                               {
                                   'class': 'form-control',
                                   'type': 'password',
                                   'id': 'password'
                               }))

class UserForm(forms.Form):
        def __init__(self, *args, **kwargs):
            perms = kwargs.pop('perms')
            instance = kwargs.pop('user',None)
            super(UserForm, self).__init__(*args, **kwargs)
            if instance:
                self.fields['first_name'].widget.attrs['value'] = instance.first_name
                self.fields['last_name'].widget.attrs['value'] = instance.last_name
                self.fields['email'].widget.attrs['value'] = instance.email
                self.fields['username'].widget.attrs['value'] = instance.username
                self.fields['username'].widget.attrs['readonly'] = True
                #Hide password inputs for security
                #del self.fields['password']
                #del self.fields['re_password']

            self.fields['permissions'].widget = forms.Select(choices=perms,
                                                             attrs={
                                                                 'class': 'form-control',
                                                                 'id': 'permissions'
                                                             })

        first_name = forms.CharField(label='Ad', max_length=45,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'first_name',
                                    }
                                ))

        last_name = forms.CharField(label='Soyad', max_length=45,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'last_name',
                                    }
                                ))


        email = forms.CharField(label='E mail', max_length=45,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 'email',
                                        'type': 'email',
                                    }
                                ))

        username = forms.CharField(label='Kullanıcı Adı', max_length=15,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'id': 'username',
                                           'validation': 'validate-username',
                                       }
                                   ))

        password = forms.CharField(label='Parola', max_length=15,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'id': 'password',
                                           'type':'password',
                                       }
                                   ))

        re_password = forms.CharField(label='Parola Tekrar', max_length=45,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'id': 're_password',
                                        'type': 'password'
                                    }
                                ))

        permissions = forms.ChoiceField(label='Yetkiler')