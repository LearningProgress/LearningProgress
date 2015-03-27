from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
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

    @property
    def exam_days(self):
        """
        Returns the days until the exam as integer.
        """
        try:
            exam_date = ExamDate.objects.get(key=self.exam)
        except ExamDate.DoesNotExist:
            value = None
        else:
            days_object = exam_date.date - timezone.now().date()
            value = days_object.days
        return value

    def progress_objects(self):
        """
        Returns some info, how many sections the user has been working on.
        Only for the website admin.
        """
        query = self.usersectionrelation_set.all()
        first_look = query.filter(progress=1).count()
        crammed = query.filter(progress=2).count()
        all_done = query.filter(progress=3).count()
        return '%d / %d / %d' % (first_look, crammed, all_done)

    progress_objects.short_description = _('Progress objects')


class ExamDate(models.Model):
    """
    Model for exam dates.
    """
    key = models.PositiveIntegerField(
        primary_key=True,
        verbose_name=ugettext_lazy('Exam key'),
        help_text=ugettext_lazy(
            'An integer with five digets. The first four digets represent the '
            'year, the last diget (1 or 2) represents the season.'))
    date = models.DateField(
        verbose_name=ugettext_lazy('Date'),
        help_text=ugettext_lazy('Choose the first date of the respective exam session.'))

    class Meta:
        ordering = ('-date',)
        verbose_name = ugettext_lazy('Date of exam')
        verbose_name_plural = ugettext_lazy('Dates of exam')

    def __str__(self):
        """
        Returns a human readable string for the exam date. It contains “Spring”
        or “Autumn” with respect to the last diget of the key.
        """
        year = self.key / 10
        if self.key % 2 == 1:
            value = _('Spring %d') % year
        else:
            value = _('Autumn %d') % year
        return '%s (%s)' % (value, str(self.date))
