from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from django.contrib.auth.forms import AuthenticationForm
# from django.forms.widgets import PasswordInput, TextInput

# The fields in this form are not in the model
# See tutorial 16 Max Goodridge Django tutorials
#
class RegistrationForm(UserCreationForm):
    # These widgets below work. I just didn't need them
    # email = forms.EmailField(widget=forms.TextInput, label="Email")
    # password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput, label="Password (again)")

    email = forms.EmailField(required=True)
    password2 = None
#
    class Meta:
        model = User
        fields = (
            # 'username',
            # 'first_name',
            # 'last_name',
            'email',
            'password1',
            # 'password2'
        )

    # def clean(self):
    #     password1 = self.cleaned_data.get("password1")
    #     try:
    #         password_validation.validate_password(password1, self.instance)
    #     except forms.ValidationError as error:
    #
    #         # Method inherited from BaseForm
    #         self.add_error("password1", error)
    #     return password1

    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     if "password" in self.cleaned_data and "password2" in self.cleaned_data:
    #         if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
    #             print "there was an error"
    #             raise forms.ValidationError("Passwords do not match. Please enter both fields again")
    #     return self.cleaned_data

    # Deleting password 2 below because I don't know how to solve the
    # ValueError situation when passwords don't match.

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
