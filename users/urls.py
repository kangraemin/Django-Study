from django.urls import path
from . import views


app_name = "users"

# Djaneiro -> django auto complete Snippet
urlpatterns = [path("login", views.LoginView.as_view(), name="login")]
