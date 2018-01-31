from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('register', register, name= 'register'),
    path('validate-username', validate_username, name='validate'),
    path('user-list-data', user_list_data, name='user_list_data'),
    path('user-list',user_list,name='user_list'),
    path('update/<str:username>',update,name='update'),
    path('delete/<str:username>',delete,name='delete')
]


