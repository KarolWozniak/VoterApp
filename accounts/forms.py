from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','group']
