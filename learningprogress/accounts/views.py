from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from . import forms
from .models import User


class UserCreateView(CreateView):
    """
    View to register a new user and log him in.
    """
    form_class = forms.UserCreateForm
    model = User
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_create_form.html'

    def form_valid(self, form):
        """
        Logs the user in after creation.
        """
        value = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return value


class UserUpdateView(UpdateView):
    """
    View to update user data for the users themselves.
    """
    form_class = forms.UserUpdateForm
    model = User
    template_name = 'accounts/user_update_form.html'
    success_url = reverse_lazy('home')
    self_pattern_name = 'user_update'

    def get_object(self, *args, **kwargs):
        """
        Returns the relevant user instance.
        """
        return self.request.user

    def get_form_kwargs(self):
        """
        Just inserts the request object into the keywords for the form
        because django does not provide this feature.
        """
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UserDeleteView(DeleteView):
    """
    View to delete oneself.
    """
    model = User
    success_url = reverse_lazy('home')

    def get_object(self, *args, **kwargs):
        """
        Returns the relevant user instance.
        """
        return self.request.user
