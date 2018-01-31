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

class RegisterForm(forms.Form):

        def __init__(self, *args, **kwargs):
            tmp = kwargs.pop('perms')
            super(RegisterForm, self).__init__(*args, **kwargs)
            self.fields['permissions'].widget = forms.Select(choices=tmp,
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


