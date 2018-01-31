from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User
from django.contrib.auth.models import Permission
from django.http import JsonResponse
from .forms import UserForm
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
        new_user.user_permissions.add(Permission.objects.get(codename=permission))
        new_user.save()

        return redirect('users:register')


    perms = list(User.get_sub_perms_from_list(perm_list=list(request.user.get_all_permissions())))
    perms = [['none','Lütfen bir yetki seçiniz ...']] + perms
    form = UserForm(perms=perms)

    context = {
        'form':form
    }
    return render(request, 'users/user_form.html', context)

def update(request,username):
    user = User.objects.get(username=username)

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))
        #user.permission = request.POST.get('permissions')
        user.save()
        return redirect('users:user_list')
    perms = list(User.get_sub_perms_from_list(perm_list=list(request.user.get_all_permissions())))
    perms = [['none', 'Lütfen bir yetki seçiniz ...']] + perms
    form = UserForm(user=user,perms=perms)
    return render(request,'users/user_update.html',{'form':form,'username':user.username})

def delete(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        user.delete()
        if not request.user.username:
            return redirect('logout')

        return redirect('users:user_list')
    else:
        labels = ['Kullanıcı Adı: ','İsim: ','Soyisim: ','Email: ']
        values = [user.username,user.first_name,user.last_name,user.email]
        context = {
            'labels': labels,
            'values': values,
            'username': user.username
        }
        if user is not None:
            return render(request, 'users/user_delete.html', context=context)

def user_list(request):
    return render(request,'users/user_list.html',{})

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

def user_list_data(request):
    users = list()
    for user in User.objects.all():
        perm_list = list(user.get_all_permissions())
        users.append(list((user.first_name,user.last_name,user.username,user.email,User.get_perm_from_list(perm_list)[1],
                          reverse('users:update', kwargs={'username': user.username}) + "," +
                          reverse('users:delete', kwargs={'username': user.username}))))

    data = {
        'data': users
    }
    return JsonResponse(data)

def home(request):
    #return HttpResponse(request.user.get_all_permissions())
    return render(request,'shared/base.html',{})