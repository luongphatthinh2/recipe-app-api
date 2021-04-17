from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin
from core_app import models
# Register your models here.

class UserAdmin(ModelAdmin):
    ordering= ('id',)
    list_display = ('email','name',)
    fieldsets = (
        (None, {'fields':('email','password')} ),
        ('Personal Info' ,{'fields':('name',)}),
        ( 'Permission', {'fields':('is_active','is_staff','is_superuser',) } ) ,
        ('Important dates', {'fields': ('last_login',) }),
    )

admin.site.register(models.User, UserAdmin)