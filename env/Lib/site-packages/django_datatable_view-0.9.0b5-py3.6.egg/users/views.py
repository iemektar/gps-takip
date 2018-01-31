from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from .forms import RegisterForm
from django.contrib.auth import logout

def register(request):

    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        permission = request.POST.get('permissions')

        new_user = User.objects.create_user(email = email, username = username, password = password,
                                            first_name = first_name ,last_name = last_name)

        perm_list = User.get_sub_perms(perm=permission)

        for item in perm_list:

            new_user.user_permissions.add(Permission.objects.get(codename=item[0]))


        return HttpResponse("Kullanıcı oluşturuldu.")


    perms = list(User.get_sub_perms_from_list(perm_list=list(request.user.get_all_permissions())))
    perms = [['none','Lütfen bir yetki seçiniz ...']] + perms
    form = RegisterForm(perms=perms)

    context = {
        'form':form
    }
    return render(request, 'users/user_form.html', context)

#superuser kullanıcıları kontrol etmiyor
#DÜZELTİLECEK!
def validate_username(request):
    username = request.POST.get('username',None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'Bu kullanıcı adı alındı. Başka bir kullanıcı adı deneyin.'
    
    return JsonResponse(data)

def home(request):
    #return HttpResponse(request.user.get_all_permissions())
    return render(request,'shared/base.html',{})