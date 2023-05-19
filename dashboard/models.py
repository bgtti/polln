from django.db import models
from website.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pw_requirement = models.BooleanField(blank=True, null=True, default=False)
    pw = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Project {self.pk}: {self.name} User: {self.user} Pw required: {self.pw_requirement}"
