from django import forms

from .models import PROGRESS_CHOICES, MockExam


class UserSectionRelationUpdateForm(forms.Form):
    """
    Form for updating a single entry.
    """
    progress = forms.ChoiceField(choices=PROGRESS_CHOICES)
    comment = forms.CharField(required=False, widget=forms.Textarea())


class MockExamForm(forms.ModelForm):
    """
    Form for new mock exams.
    """
    class Meta:
        model = MockExam
        fields = ('branch', 'mark', 'date')
