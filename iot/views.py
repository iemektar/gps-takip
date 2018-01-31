from django.shortcuts import render,HttpResponse,reverse, redirect
from .forms import IoTForm
from .models import IoT
from django.http import JsonResponse
from django.core.serializers import serialize

#Create a new IoT
def create_iot(request):
    context = {}
    if request.method == "POST":
        serial_no = request.POST.get('serial_no')
        plate_no = request.POST.get('plate_no')
        is_active = str(False)

        if len(plate_no) > 0:
            is_active = str(True)

        iot = IoT.objects.create(serial_no=serial_no, plate_no=plate_no, is_active=is_active)
        context.setdefault('message_type',1)
        context.setdefault('message_title','BİLGİLENDİRME!')
        context.setdefault('message_content','Yeni Cihaz Başarıyla Eklendi.')

    form = IoTForm()
    context.setdefault('form',form)
    return render(request, 'iot/iot_create.html', context)

#Returns a data table
def iot_list(request):
    return render(request,'iot/iot_list.html',{})


def update(request, serial_no):
    iot = IoT.objects.get(serial_no=serial_no)
    if request.method == 'POST':
        plate_no = request.POST.get('plate_no')
        if plate_no is not iot.plate_no:
            iot.plate_no = plate_no
            iot.is_active = True if len(plate_no) > 0 else False
            iot.save()
        return redirect('iot:iot_list')

    form = IoTForm(instance=iot)
    return render(request, 'iot/iot_update.html', {'form':form, 'serial_no':serial_no})


def delete(request, serial_no):
    iot = IoT.objects.get(serial_no=serial_no)
    if request.method == 'POST':
        iot.delete()
        return redirect('iot:iot_list')
    else:
        labels = ['Seri No:','Plaka No:']
        values= [iot.serial_no, iot.plate_no]
        context = {
            'labels': labels,
            'values': values,
            'serial_no': iot.serial_no
        }
        if iot is not None:
            return render(request,'iot/iot_delete.html',context=context)

#AJAX

#Validation
def validate_serial_no(request):
    serial_no = request.POST.get('serial_no', None)
    data = {
        'is_taken': IoT.objects.filter(serial_no__iexact=serial_no).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Bu seri numaraya kayıtlı cihaz bulunmaktadır. Lütfen başka bir tane giriniz.'
    return JsonResponse(data)


def validate_plate_no(request):

    plate_no = request.POST.get('plate_no', None)
    data = {
        'is_taken': IoT.objects.filter(plate_no__iexact=plate_no).exists()
    }
    if request.POST.get('type') == 'update':
        if data['is_taken']:
            serial_no = request.POST.get('serial_no')
            if IoT.objects.get(serial_no__iexact=serial_no).plate_no == plate_no:
                data['is_taken'] = False

    if data['is_taken']:
        data['error_message'] = 'Bu plaka numarası başka cihaz tarafından kullanılmaktadır. Lütfen başka bir tane giriniz.'
    return JsonResponse(data)

#Data Table
def iot_list_data(request):

    iots = list()
    for iot in IoT.objects.all():
        iots.append(list((iot.serial_no,iot.plate_no,iot.is_active,'ut1',
                          reverse('iot:iot_update', kwargs={'serial_no': iot.serial_no}) + ","+
                          reverse('iot:iot_delete', kwargs={'serial_no': iot.serial_no}))))

    data = {
        'data': iots
    }
    return JsonResponse(data)

