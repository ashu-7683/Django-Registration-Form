from app.models import *
from django import forms


class UserMF(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields=['username','password','email']
        #exclude=['username','password','email']
        help_texts={'username':'','password':'It will be hidden'}
        widgets={'password':forms.PasswordInput()}
        
        
class ProfileMF(forms.ModelForm):
    class Meta:
        model=Profile
        #fields='__all__'
        exclude=['username']