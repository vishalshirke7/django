from django import forms
from .models import User
from signup.random_string_generator import random_string_generator_c


class SignupForm(forms.Form):
    fname = forms.CharField(label="First Name", max_length=50,required=True)
    lname = forms.CharField(label="Last Name", max_length=50,required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(user_email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already in use.')


class LoginForm(forms.Form):
    username = forms.CharField(label="Email/Username", max_length=50,required=True)
    password = forms.CharField(label="Password", max_length=10,widget=forms.PasswordInput,required=True)

    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        ranstrng = random_string_generator_c()
        userpasw = ranstrng.hash_password(password)

        try:
            user = User.objects.get(user_email=username)
            if not user.user_isactive:
                raise forms.ValidationError("Account Not verified !")
            elif user.user_password != userpasw:
                raise forms.ValidationError("Sorry, wrong username or password !")
        except User.DoesNotExist:
                raise forms.ValidationError("Invalid Login")
        return self.cleaned_data


class PasswordReset(forms.Form):
    email = forms.CharField(label="email", max_length=50, required=True)

    class Meta:
        model = User

    def clean(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(user_email=email)
            if not user.user_isactive:
                raise forms.ValidationError("Account Not verified !")
        except User.DoesNotExist:
            raise forms.ValidationError("This email-address doesn't exist!")
        return self.cleaned_data


class PasswordForm(forms.Form):
    password = forms.CharField(label="New Password", max_length=10, widget=forms.PasswordInput, required=True)
    repassword = forms.CharField(label="Re-type Password", max_length=10, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User

    def clean_repassword(self):
        psw = self.cleaned_data.get('password')
        repsw = self.cleaned_data.get('repassword')
        if psw != repsw:
            raise forms.ValidationError("Password doesn't match!")
        return self.cleaned_data


class UpdateForm(forms.Form):
    fname = forms.CharField(label="First Name", max_length=50)
    lname = forms.CharField(label="Last Name", max_length=50)

    class Meta:
        model = User


class ChangePassword(forms.Form):
    prepass = forms.CharField(label="Previous Password", max_length=10, widget=forms.PasswordInput, required=True)
    password = forms.CharField(label="New Password", max_length=10, widget=forms.PasswordInput, required=True)
    repassword = forms.CharField(label="Re-type Password", max_length=10, widget=forms.PasswordInput, required=True)

    class Meta:
        model = User

    def clean_prepass(self):
        prepsw = self.cleaned_data.get('prepass')
        ranstrng = random_string_generator_c()
        userpasw = ranstrng.hash_password(prepsw)
        try:
            user = User.objects.get(user_password=userpasw)
            if user.user_password == userpasw:
                pass
        except User.DoesNotExist:
            raise forms.ValidationError("Wrong Password")
        return self.cleaned_data

    def clean_repassword(self):
        psw = self.cleaned_data.get('password')
        repsw = self.cleaned_data.get('repassword')
        if psw != repsw:
            raise forms.ValidationError("Password doesn't match!")
        return self.cleaned_data