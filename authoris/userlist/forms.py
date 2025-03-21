from django import forms
from .models import Users

class LoginForm(forms.Form):
    email = forms.EmailField()  # Поле для email
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для пароля

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Users
        fields = ['email', 'password', 'password_confirm']

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:  # Исправлено на password_confirm
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_confirm']  # Исправлено на password_confirm
    