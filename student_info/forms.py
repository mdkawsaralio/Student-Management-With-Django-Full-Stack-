from django import forms
from django.forms import inlineformset_factory
from .models import Student, Result


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude=['user']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['exam', 'subject', 'marks']


ResultFormset = inlineformset_factory(
    Student,
    Result,
    form=ResultForm,
    extra=1,
    can_delete=False
)
UpdateResultFormset = inlineformset_factory(
    Student,
    Result,
    form=ResultForm,
    extra=0,
    can_delete=False
)