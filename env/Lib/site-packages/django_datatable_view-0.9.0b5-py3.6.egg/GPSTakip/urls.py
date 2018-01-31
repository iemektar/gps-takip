"""GPSTakip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth import views
from users.forms import LoginForm

import users.urls as user_urls
import home.urls as home_urls
import iot.urls as iot_urls

urlpatterns = [
    path('',views.login,{'template_name': 'users/login.html','authentication_form':LoginForm,
                         'redirect_authenticated_user': True},name='login'),
    path('logout',views.logout,name='logout'),
    path('home', include(home_urls)),
    path('users/',include(user_urls)),
    path('iot/',include(iot_urls))
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
