from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "poll"

# silly urls here because the first url accepts a string. If second url were, for instance, poll/check, it would 
# try to open the poll url of a project instead, and give an error. Since the url to the poll should be as simple as possible,
# I decided not to change it. The other urls are in any case only sending or receiving data to/from a JS function (not used for browsing).
urlpatterns = [
    path("<str:prj>", views.index, name="index"),
    path("check_if_poll_open/check", views.check_if_poll_open, name="check_if_poll_open"),
    path("get_answers/answer", views.get_answers, name="get_answers"),
    path("check_poll_password/password",
            views.check_poll_password, name="check_poll_password"),
]
urlpatterns += staticfiles_urlpatterns()
