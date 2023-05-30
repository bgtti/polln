from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "poll"

urlpatterns = [
    path("<str:prj>", views.index, name="index"),
    # path("get_answers", views.get_answers, name="get_answers"),
]
urlpatterns += staticfiles_urlpatterns()
