from django import forms
from django.contrib.auth.models import User, Group


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'group']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

            group = self.cleaned_data['group']
            user.groups.add(group)

        return user