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

    # If use clean ( not clean_fields ) have to add error to related field about errors
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                # If use clean ( not clean_fields ) have to return cleaned data always
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

    # If you want to check variable is valid, you have to set method name clean_VARIABLE() ~~ !
    # This clean ~~ method clean up data automatically
    # def clean_email(self):
    #     # print("clean email")
    #     # print(self.cleaned_data)
    #     email = self.cleaned_data.get("email")
    #     print(email)
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         # raise error ( show error message ) in this form ( this case, this error will be shown email form )
    #         raise forms.ValidationError("User does not exist")

    # def clean_password(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             return password
    #         else:
    #             raise forms.ValidationError("Password is wrong")
    #     except models.User.DoesNotExist:
    #         pass
