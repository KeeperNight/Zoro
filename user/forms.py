from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':15, 'maxlength':50}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'size':15, 'maxlength':20}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'size':15, 'maxlength':20}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':30, 'maxlength':50}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':20}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'size':20, 'maxlength':20}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'quote', 'address', 'city', 'country', 'zipcode', 'aboutme']

