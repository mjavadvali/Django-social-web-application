from django import forms 
from .models import User

# class Loginform(forms.Form):
#     username = forms.CharField(max_length=150, required=True)
#     password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.EmailInput, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password", max_length=100, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Repeat password", max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
