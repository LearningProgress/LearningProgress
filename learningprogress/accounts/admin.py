from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.models import Group

from .models import ExamDate, User


class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email', 'is_active',
                       'is_staff', 'exam', 'last_login', 'date_joined')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'exam')}),)
    list_display = ('username', 'date_joined', 'last_login', 'is_active', 'is_staff', 'progress_objects')
    list_filter = ()
    search_fields = ('username', 'email')


admin.site.register(ExamDate)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
