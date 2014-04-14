from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy


class User(AbstractUser):
    """
    Model for customized user.
    """
    exam = models.PositiveIntegerField(
        null=True,
        verbose_name=ugettext_lazy('Exam'),
        help_text=ugettext_lazy(
            'An integer with five digets. The first four digets represent the '
            'year, the last diget (1 or 2) represents the season.'))

    def has_perm(self, perm, obj=None):
        """
        Returns always True because we won't use Django's permission system.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Returns always True because we won't use Django's permission system.
        """
        return True
