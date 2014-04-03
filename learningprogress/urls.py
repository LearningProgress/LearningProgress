from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()


class HomeView(TemplateView):
    """
    Base view for the home page.
    """
    template_name = 'home.html'
    self_pattern_name = 'home'


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('learningprogress.accounts.urls')),
    #url(r'^learning_progress/', include('leo.learning_progress.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
