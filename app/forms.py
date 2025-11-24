from django import forms
from app.models import *
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        #fields='__all__'
        fields=['username','password','email']
        help_texts={'username':None}
        widgets={'password':forms.PasswordInput()}

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        #fields='__all__'
        exclude=['username']




class EmailForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6)

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
'''
While we are sending Parent Tables FOrm Object and
Child Tables FOrm Object into same HTML page 
then we should not represent Parent Tables column in 
Input Elements
'''