from django.contrib import admin
from dashboard.models import Project, Question, Respondent, Answer, Result

# Register your models here.
admin.site.register(Project)
admin.site.register(Question)
admin.site.register(Respondent)
admin.site.register(Answer)
admin.site.register(Result)
