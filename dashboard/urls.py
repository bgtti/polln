from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("/<message>", views.index, name="index"),
    path("add_project", views.add_project, name="add_project"),
    path("project/<int:id>", views.project, name="project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
]
