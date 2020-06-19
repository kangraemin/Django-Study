from django import forms
from . import models

# CSRF -> Cross Site Request Forgery : 사이트간 요청 위조
# When login, website gives to user cookies
# If facebook gives to user cookies, when user try to login to facebook, user send cookies through browser every request
# Assum that user try to connect website is not facebook and that website has crazy button / js .... things.
# And If user clicked strange button / js file -> website button request something to facebook.
# That request is sended in user's browser -> send cookies to facebook automatically.
# Simply speaking, submitting in strange website not user's website.
# So, django prevent this attacks using csrf_token in django template forms.
# CSRF token is used for verify this token is comming from safe website ( our website ) not strange website.


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)  # Not PasswordInput() !

    # If you want to check variable is valid, you have to set method name clean_VARIABLE() ~~ !
    # This clean ~~ method clean up data automatically
    def clean_email(self):
        # print("clean email")
        # print(self.cleaned_data)
        email = self.cleaned_data.get("email")
        print(email)
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        print("clean password")
        return "dffff"
