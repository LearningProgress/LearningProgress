from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class ProgressAppConfig(AppConfig):
    name = 'learningprogress.progress'
    verbose_name = ugettext_lazy('Learning Progress')
