from django import forms
from .models import Users

class LoginForm(forms.Form):
    email = forms.EmailField()  # Поле для email
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для пароля

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('email', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    