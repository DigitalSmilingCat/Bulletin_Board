from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class BaseRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    password1 = forms.CharField(label="Choose password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class CodeLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    code = forms.CharField(max_length=30)


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 17%'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )