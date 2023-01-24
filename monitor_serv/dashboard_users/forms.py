from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.contrib.auth import forms, models
from django.forms import fields
from . import models as du_models


class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.UserCreationForm):
    email = fields.EmailField(required=True)

    class Meta:
        model = du_models.CustomUser
        fields = 'username first_name last_name email password1 password2'.split()


class NewUserForm(forms.UserCreationForm):
    email = fields.EmailField(required=True)

    class Meta:
        model = du_models.CustomUser
        fields = 'username first_name last_name email password1 password2'.split()

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user


class LoginForm(forms.AuthenticationForm):
    class Meta:
        model = models.User
        fields = "username password".split()
