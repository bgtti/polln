from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "present"

urlpatterns = [
    path("<str:prj>", views.index, name="index"),
]
urlpatterns += staticfiles_urlpatterns()
