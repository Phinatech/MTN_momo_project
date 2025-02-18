from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.contrib.auth.forms import PasswordChangeForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'validate',  
        'id': 'reg_user_name',
    }))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'validate',  
        'id': 'first_name',
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'validate',  
        'id': 'last_name',
    }))
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'validate',  
        'id': 'reg_user_name'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': '',  
        'id': 'reg_pass_word',
        'onkeyup': 'validate()'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': '',  
        'id': 're_pass_word',
        'onkeyup': 'validate()'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "cover_image", "phone", "location", "address_line1", "address_line2", "zipcode"]
        


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter current password"}),
        label="Current Password",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter new password"}),
        label="New Password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm new password"}),
        label="Confirm New Password",
    )
