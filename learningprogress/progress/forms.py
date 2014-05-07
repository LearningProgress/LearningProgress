from django import forms
from django.utils.translation import ugettext_lazy

from .models import PROGRESS_CHOICES, MockExam


class UserSectionRelationUpdateForm(forms.Form):
    """
    Form for updating a single entry.
    """
    progress = forms.ChoiceField(
        label=ugettext_lazy('Progress'),
        choices=PROGRESS_CHOICES)
    comment = forms.CharField(
        label=ugettext_lazy('Comment'),
        required=False,
        widget=forms.Textarea())


class MockExamForm(forms.ModelForm):
    """
    Form for new mock exams.
    """
    class Meta:
        model = MockExam
        fields = ('branch', 'mark', 'date')
