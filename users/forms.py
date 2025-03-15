from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tasks.forms import StyleFormMixin 


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
             self.fields[fieldname].help_text = None
    

class CustomRegistrationForm(StyleFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'password1', 'confirm_password', 'email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError('Email is already in use')
        return email
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long')
           
        
        if not re.search(r'[A-Z]', password1):
            errors.append('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password1):
            errors.append('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', password1):
            errors.append('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*()_+=-]', password1):
            errors.append('Password must contain at least one special character')
        
        
        if errors:
            raise forms.ValidationError(errors)

        return password1
    
    
    
    def clean(self): 
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        if password1 != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

            
        
    
