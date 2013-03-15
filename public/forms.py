from core.models import Repository
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=512)
    password = forms.CharField(max_length=512, widget=forms.PasswordInput())
    
class CreateAccountForm(forms.ModelForm):    
    class Meta:
        model = User    
        fields = [
            "email",
            "username",
            "password"
        ]
        
        widgets = {
            "password" : forms.PasswordInput()
        }
        
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput())        
    
    def clean(self):
        if self.cleaned_data.get('confirm_password') != self.cleaned_data.get('password'):
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
            
class CreateRepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        
    def __init__(self, request, *args, **kwargs):
        self.request = request        
        super(CreateRepositoryForm, self).__init__(*args, **kwargs)        
        
