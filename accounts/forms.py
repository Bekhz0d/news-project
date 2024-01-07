# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser


# class CustomUserForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'age')
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'age',)


from django import forms
from django.contrib.auth.models import User
from .models import Profile


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol",
                               widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Parolni takrorlang",
                                 widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', "first_name", "email"]

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("Parollar o'zaro mos emas!")
        return data['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]