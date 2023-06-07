from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.index, name="index"),
    path("guide", views.guide, name="guide"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
]