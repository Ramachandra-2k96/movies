# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UploadFileForm(forms.Form):
    file = forms.FileField()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter password'})
