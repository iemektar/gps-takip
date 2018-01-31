from django.urls import path
from .views import *

app_name = 'iot'
urlpatterns = [
    path('create', create_iot, name='create_iot'),
    path('validate-serial-no', validate_serial_no, name='validate_serial_no'),
    path('validate-plate-no', validate_plate_no, name='validate_plate_no'),
    path('iot-list',BootstrapTemplateOfficialDatatableView.as_view(),name='iot_list')
]