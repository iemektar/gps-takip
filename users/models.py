from django.db import models,migrations
from django.contrib.auth.models import User as django_user
from django.contrib.auth.models import UserManager as django_user_manager

class User(django_user):
    perms = (
        ('ut1', "user type 1"),
        ('ut2', "user type 2"),
        ('ut3', "user type 3"),
        ('ut4', "user type 4")
    )
    class Meta:
        permissions = (
            ('ut1', "user type 1"),
            ('ut2', "user type 2"),
            ('ut3', "user type 3"),
            ('ut4', "user type 4")
        )

    @classmethod
    def get_custom_permissions(cls):
        return cls.perms
    @classmethod
    def get_sub_perms(cls,perm):
        i = 0
        while (i < len(cls.perms)):
            if cls.perms[i][0] == perm:
                return cls.perms[i:]
            i+=1

    @classmethod
    def get_sub_perms_from_list(cls,perm_list):
        i = 0
        while(i < len(cls.perms)):
            if 'users.' + cls.perms[i][0] in perm_list:
                return cls.perms[i: ]
            i+=1
        return list()

    @classmethod
    def get_perm_from_list(cls, perm_list):
        i = 0
        while (i < len(cls.perms)):
            if 'users.' + cls.perms[i][0] in perm_list:
                return cls.perms[i]
            i += 1
        return cls.perms[0]


