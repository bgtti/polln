from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path('generate_qr_code/<str:url>/', views.generate_qr_code, name='generate_qr_code'),
    path("add_project", views.add_project, name="add_project"),
    path("project/<int:id>", views.project, name="project"),
    path("edit_project/<int:id>", views.edit_project, name="edit_project"),
    path("delete_project/<int:id>", views.delete_project, name="delete_project"),
    path("add_question", views.add_question, name="add_question"),
    path("question_order", views.question_order, name="question_order"),
    path("edit_question/<int:id>", views.edit_question, name="edit_question"),
    path("delete_question/<int:id>", views.delete_question, name="delete_question"),
    path("open_poll/<int:id>", views.open_poll, name="open_poll"),
    path("close_poll/<int:id>", views.close_poll, name="close_poll"),
    # path("get_answers", views.get_answers, name="get_answers"),
    # path("live_vote_count/<int:id>", views.live_vote_count, name="live_vote_count"),
]
urlpatterns += staticfiles_urlpatterns()