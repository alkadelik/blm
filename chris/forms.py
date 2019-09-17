from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from django.contrib.auth.forms import AuthenticationForm
# from django.forms.widgets import PasswordInput, TextInput

# The fields in this form are not in the model
# See tutorial 16 Max Goodridge Django tutorials
#
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
#
    class Meta:
        model = User
        fields = (
            # 'username',
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        # user.first_name = self.cleaned_data['first_name']
        # user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = user.email

        if commit:
            user.save()

        return user

# Used with AuthenticationForm
# class CustomAuthForm(AuthenticationForm):
#     username = forms.CharField(widget=TextInput(attrs={"class":"validate", "placeholder": "Email"}))
#     password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )
