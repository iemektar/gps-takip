from django.shortcuts import render,HttpResponse
from .forms import CreateIoTForm
from .models import IoT
from django.http import JsonResponse
def create_iot(request):

    if request.method == "POST":
        serial_no = request.POST.get('serial_no')
        plate_no = request.POST.get('plate_no')
        is_active = str(False)

        if len(plate_no) > 0:
            is_active = str(True)

        iot = IoT.objects.create(serial_no=serial_no, plate_no=plate_no, is_active=is_active)
        return HttpResponse("Cihaz Eklendi.")
    form = CreateIoTForm()
    context = {
        'form': form
    }
    return render(request, 'iot/iot_create.html', context)

def validate_serial_no(request):
    serial_no = request.POST.get('serial_no', None)
    data = {
        'is_taken': IoT.objects.filter(serial_no__iexact=serial_no).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Bu seri numaraya kayıtlı cihaz bulunmaktadır. Lütfen başka bir tane giriniz.'
    return JsonResponse(data)


def validate_plate_no(request):
    serial_no = request.POST.get('plate_no', None)
    data = {
        'is_taken': IoT.objects.filter(plate_no__iexact=serial_no).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Bu plaka numarası başka cihaz tarafından kullanılmaktadır. Lütfen başka bir tane giriniz.'
    return JsonResponse(data)


class BootstrapTemplateOfficialDatatableView(DatatableView):
    model = IoT
    datatable_options = {
        'structure_template': "iot/iot_list.html",
        'columns': [
            'id',
            'headline',
            'blog',
            'pub_date',
        ],
    }