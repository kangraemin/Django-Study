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


# Model form makes that don't need to check field type in models ( model form -> forms connected model)
# Nico -> don'y use modelform in sign up form ( because nico want to customize more than this code )
class SignUpForm(forms.ModelForm):

    # search django model form meta class
    # Model form can validate unique value is unique
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email", "birthdate")

    # User model don't have password not encrypted ( Password user models has is encrypted password )
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm password"
    )  # label -> change form's views in front end

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # There is already save method in ModelfForm ( form does not have save method )
    # save -> ojbect save
    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # Commit = false -> Create object but don't put it in database
        user = super().save(commit=False)
        user.username = email
        # Set user's password / Adapt password hashing / Don't save user object
        user.set_password(password)
        user.save()


# class SignUpForm(forms.Form):

#     # Django read fields up to down and call cleaning method with read fields data
#     # So If django read password fields -> python doesn't know password1 variables ( because before cleaning password1 )
#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(
#         widget=forms.PasswordInput, label="Confirm password"
#     )  # label -> change form's views in front end

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("User already exist with that email")
#         except models.User.DoesNotExist:
#             return email

#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")

#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password

#     def save(self, *args, **kwargs):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")

#         # models.User.objects.create()  # Nope ! password must be encrypted
#         user = models.User.objects.create_user(email, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()
