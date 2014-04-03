from django import forms
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from .models import User


def get_exam_choices(extra=None):
    """
    Returns a list of two-tuples with actual exam dates for form use.
    Extra may be a valid exam integer, e. g. 20082. If it is given, a
    respective entry is added to the return value if missing.
    """
    number_of_years = 8  # Change this to get more or less entries in the form widget.
    this_year = timezone.now().year
    choices = []
    for year in range(this_year, this_year + number_of_years):
        choices.append((year * 10 + 1, _('Spring %d') % year))
        choices.append((year * 10 + 2, _('Autumn %d') % year))
    if extra:
        extra_year = int(extra / 10)
        if extra % 2 == 1:
            text = _('Spring %d') % extra_year
        else:
            text = _('Autumn %d') % extra_year
        if extra_year < this_year:
            choices.insert(0, (extra, text))
        elif extra_year > this_year + number_of_years - 1:
            choices.append((extra, text))
    return choices


class UserCreateForm(forms.ModelForm):
    """
    A form for creating new users. Includes repeated password fields.
    """
    password1 = forms.CharField(label=ugettext_lazy('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=ugettext_lazy('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """
        Inserts the exam form field.
        """
        value = super().__init__(*args, **kwargs)
        self.fields['exam'] = forms.ChoiceField(label=ugettext_lazy('Exam'), choices=get_exam_choices())
        return value

    def clean_password2(self):
        """
        Checks that the two password entries match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        """
        Saves the form including the exam value and the provided password in
        hashed format.
        """
        user = super().save(commit=False)
        user.exam = self.cleaned_data['exam']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    A form for updating users. Password change is not possible with this
    form.
    """
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, request, *args, **kwargs):
        """
        Pops the request argument, inserts the exam form field and
        its initial value.
        """
        self.request = request
        value = super().__init__(*args, **kwargs)
        exam = self.request.user.exam
        self.fields['exam'] = forms.ChoiceField(
            label=ugettext_lazy('Exam'),
            choices=get_exam_choices(extra=exam))
        self.initial['exam'] = exam
        return value

    def save(self, commit=True):
        """
        Saves the form data including the exam value.
        """
        user = super().save(commit=False)
        user.exam = self.cleaned_data['exam']
        if commit:
            user.save()
        return user
