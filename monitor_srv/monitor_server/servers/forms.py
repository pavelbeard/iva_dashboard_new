from django.views.generic import edit
from django import forms
from . import models


class AddServerForm(edit.FormView):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = models.Target
