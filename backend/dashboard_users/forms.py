from dashboard_users.models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# class SignupForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.UserCreationForm):
#     email = fields.EmailField(required=True)
#
#     class Meta:
#         model = du_models.CustomUser
#         fields = 'username first_name last_name email password1 password2'.split()


class NewUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Введите имя пользователя. "
                                                       "Оно должно содержать английские буквы. "}
    ), label="Имя пользователя:")
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Введите имя."}
    ), label="Имя:")
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Введите фамилию."}
    ), label="Фамилия:")
    email = forms.CharField(widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Введите email. "
                                                       "Формат: username@example.com"}
    ), label="E-Mail:")
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Введите пароль. "
                                                       "Пароль должен состоять из цифр, "
                                                       "заглавных латинских букв и символов."}
    ), label="Пароль:")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Введите подтверждение."}
    ), label="Подтверждение")

    class Meta:
        model = CustomUser
        fields = 'username first_name last_name email password1 password2'.split()

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name'].capitalize()
        user.last_name = self.cleaned_data['last_name'].capitalize()
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Введите имя пользователя. "
                                                       "Оно должно содержать английские буквы. "}
    ), label="Имя пользователя:")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Введите пароль."}
    ), label="Пароль:")

    class Meta:
        model = CustomUser
        fields = "username password".split()
        
    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['username'].lower()
        return super().clean()
