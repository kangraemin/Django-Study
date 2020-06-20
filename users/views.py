import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


# Login view -> forms for login but toooo many for that so, difficult to customize so use FormView
# nico prefer Form view than Loginview
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # reverse_lazy -> is not going to exectue immidiatly is loaded is needed
    # because url did not have loaded at initializing moment so use reverse_lazy
    success_url = reverse_lazy("core:home")
    initial = {"email": "remin1994@gmail.com"}

    # Only need to do is Chevk form is valid !
    # Form file -> form_vaild() !! ( don't need validate variable )
    # If success -> goes to success_url
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # def get(self, request):
    #     form = forms.LoginForm(initial={"email": "kang@rae.com"})
    #     return render(request, "users/login.html", {"form": form})

    # def post(self, request):
    #     form = forms.LoginForm(request.POST)
    #     if form.is_valid():
    #         # cleaned data -> result after cleaning data If clean method didn't return anything, it delete that fields
    #         print(form.cleaned_data)
    #         # authenticate -> return user with other task ( cookies ... ) and need to give username ( not email ) / password for params
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(request, username=email, password=password)
    #         if user is not None:
    #             print("is user")
    #             login(request, user)
    #             return redirect(reverse("core:home"))
    #     return render(request, "users/login.html", {"form": form})


# fbv method
# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "kang@rae.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             # cleaned data -> result after cleaning data If clean method didn't return anything, it delete that fields
#             print(form.cleaned_data)
#             # authenticate -> return user with other task ( cookies ... ) and need to give username ( not email ) / password for params
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 print("is user")
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

    # def login_view(request):
    #     if request.method == "GET":

    #     if request.method == "POST": ~~


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Nicoas",
        "last_name": "Serr",
        "email": "itn@las.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add success message
    except models.User.DoesNotExist:
        ## to do : add error message
        pass
    return redirect(reverse("core:home"))


""" 
1. User clicked github_login button 
2. Url connect user to this github_login function view
3. View redirect user to github 
4. When user login in github, github send user to our call back url ( redirect Authorization callback URL )
"""


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    scope = "read:user"  # choose scope we must have things
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get(
            "code", None
        )  # code -> If you use code or receive code long time ( about 10 min ) ago, code will be useless code
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                api_request = requests.get(
                    f"https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # api_request.status_code ( it can use to check response is OK but some api send OK code although they have error in response )
                profile_json = api_request.json()
                username = profile_json.get("login", None)
                print(profile_json)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    print(name, email, bio)
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                        else:  # trying to login in using Github account
                            pass
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()  # Marks the user as having no password set / Doesn't save the User object
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))

