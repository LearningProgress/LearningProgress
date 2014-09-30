from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class AccountsAppConfig(AppConfig):
    name = 'learningprogress.accounts'
    verbose_name = ugettext_lazy('Accounts')
