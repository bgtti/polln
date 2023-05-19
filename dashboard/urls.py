from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("msg/<message>", views.index, name="index"),
    path("add_project", views.add_project, name="add_project"),
    path("project/<int:id>", views.project, name="project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
]
urlpatterns += staticfiles_urlpatterns()