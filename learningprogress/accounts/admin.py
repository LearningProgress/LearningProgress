from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm
from django.contrib.auth.models import Group

from .models import ExamDate, User


class UserCreationForm(_UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    # The method clean_username is just copied as is from
    # django.contrib.auth.forms.UserCreationForm because we have to patch
    # the User class in line 101 and 102.
    # TODO: Refactor this when upgrading to Django >= 1.8

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username')


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
    add_form = UserCreationForm


admin.site.register(ExamDate)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
