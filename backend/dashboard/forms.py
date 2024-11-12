from django import forms

from dashboard.models import Target


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = '__all__'

    password = forms.CharField(widget=forms.PasswordInput(), required=False)