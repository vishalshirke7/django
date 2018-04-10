from django import forms
from .models import User

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
            # Unable to find a user, this is fine
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
        try:
            user = User.objects.get(user_email=username)
            if user.user_isactive == False:
                raise forms.ValidationError("Account Not verified !")
            elif user.user_password != password:
                raise forms.ValidationError("Sorry, wrong username or password !")
        except User.DoesNotExist:
                raise forms.ValidationError("Invalid Login")
        return self.cleaned_data

    #def login_f(self, request):
     #   username = self.cleaned_data.get('username')
      #  password = self.cleaned_data.get('password')
       # user = auth.authenticate(username=username, password=password)
        #return user
        
