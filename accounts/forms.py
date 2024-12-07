from tokenize import Comment

from django import  forms
from django.contrib.auth.models import User

from accounts.models import Profile


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'placeholder':'Enter your name'}))
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password_1 = forms.CharField(max_length=50 , widget=forms.PasswordInput(attrs={'placeholder' : 'password...'}))
    password_2 = forms.CharField(max_length=50 , widget=forms.PasswordInput(attrs={'placeholder' : 'password...'}))
    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError("Username already exists")
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    def clean_password_2(self):
        pass1 = self.cleaned_data['password_1']
        pass2 = self.cleaned_data['password_2']
        if pass1 != pass2:
            raise forms.ValidationError("Passwords must match")
        elif len(pass2) < 8 :
            raise forms.ValidationError("Password must be at least 8 characters")
        elif not any (x.isupper() for x in pass2):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        return pass2

class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address')