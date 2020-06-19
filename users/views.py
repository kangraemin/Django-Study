from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "kang@rae.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # cleaned data -> result after cleaning data If clean method didn't return anything, it delete that fields
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form": form})

    # def login_view(request):
    #     if request.method == "GET":

    #     if request.method == "POST": ~~
