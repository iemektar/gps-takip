from django.urls import path
from .views import *

app_name = 'iot'
urlpatterns = [
    path('create', create_iot, name='iot_create'),
    path('validate-serial-no', validate_serial_no, name='validate_serial_no'),
    path('validate-plate-no', validate_plate_no, name='validate_plate_no'),
    path('iot-list',iot_list,name='iot_list'),
    path('iot-list-data',iot_list_data,name='iot_list_data'),
    path('delete/<str:serial_no>',delete, name='iot_delete'),
    path('update/<str:serial_no>',update, name='iot_update')
]