from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy
from mptt import models as mptt_models

from learningprogress.accounts.models import User


class Section(mptt_models.MPTTModel):
    """
    Model for sectioning the curriculum.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=ugettext_lazy('Name'))
    parent = mptt_models.TreeForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        verbose_name=ugettext_lazy('Parent section'))
    weight = models.IntegerField(
        default=0,
        verbose_name=ugettext_lazy('Weight'),
        help_text=ugettext_lazy('Use this for ordering elements.'))
    scores = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=ugettext_lazy('Learning scores'),
        help_text=ugettext_lazy('Choose a value from 1 to 100. Only relevant for elements without children.'))
    notes = models.TextField(
        blank=True,
        verbose_name=ugettext_lazy('Notes'))
    users = models.ManyToManyField(
        User,
        through='UserSectionRelation')

    class Meta:
        verbose_name = ugettext_lazy('Section')
        verbose_name_plural = ugettext_lazy('Sections')

    class MPTTMeta:
        order_insertion_by = ['weight', 'name']

    def __str__(self):
        return self.name


PROGRESS_CHOICES = (
    (0, ugettext_lazy('Nothing done')),
    (1, ugettext_lazy('First look')),
    (2, ugettext_lazy('Crammed')),
    (3, ugettext_lazy('All done')))


class UserSectionRelation(models.Model):
    """
    Many-to-many relationship between an user and an section in the
    curriculum.
    """
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section, related_name='usersectionrelation')
    progress = models.IntegerField(default=0, choices=PROGRESS_CHOICES)
    comment = models.TextField()

    class Meta:
        unique_together = (('user', 'section'),)
        verbose_name = ugettext_lazy('Relation between an user and a section')

    def __str__(self):
        return '%s – %s' % (self.user, self.section)


class MockExamBranch(models.Model):
    """
    Model for branches for mock exams.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=ugettext_lazy('Name'))
    weight = models.IntegerField(
        default=0,
        verbose_name=ugettext_lazy('Weight'),
        help_text=ugettext_lazy('Use this for ordering elements.'))

    class Meta:
        ordering = ('weight', 'name')
        verbose_name = ugettext_lazy('Mock exam branch')
        verbose_name_plural = ugettext_lazy('Mock exam branches')

    def __str__(self):
        return self.name


class MockExam(models.Model):
    """
    Model for mock exams.
    """
    user = models.ForeignKey(User)
    branch = models.ForeignKey(
        MockExamBranch,
        verbose_name=ugettext_lazy('Branch'))
    mark = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(18)],
        verbose_name=ugettext_lazy('Mark'))
    date = models.DateField()

    class Meta:
        ordering = ('branch', 'date')

    def __str__(self):
        return '%s – %s' % (self.user, self.branch)
