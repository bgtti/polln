from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "present"

urlpatterns = [
    path("<str:prj>", views.index, name="index"),
    path("live_vote_count/<int:id>", views.live_vote_count, name="live_vote_count"),
]
urlpatterns += staticfiles_urlpatterns()
