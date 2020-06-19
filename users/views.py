from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "kang@rae.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form.is_valid())
        return render(request, "users/login.html", {"form": form})

    # def login_view(request):
    #     if request.method == "GET":

    #     if request.method == "POST": ~~
