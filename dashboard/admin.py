from django.contrib import admin
# from website.models import User
from dashboard.models import Project, Question, Answer

# Register your models here.
# admin.site.register(User)
admin.site.register(Project)
admin.site.register(Question)
admin.site.register(Answer)
