from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns(
    '',
    # Login and logout
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': 'home'},
        name='logout'),
    # Password administration
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change_form.html'},
        name='password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),
    url(r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password_reset_confirm/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'),
    # User administration
    url(r'^register/$',
        views.UserCreateView.as_view(),
        name='user_create'),
    url(r'^update/$',
        login_required(views.UserUpdateView.as_view()),
        name='user_update'),
    url(r'^delete/$',
        login_required(views.UserDeleteView.as_view()),
        name='user_delete'))
