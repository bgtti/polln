from django.db import models
from website.models import User


class Project(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=100)
    pw_requirement = models.BooleanField(blank=True, null=True, default=False)
    pw = models.CharField(max_length=30, blank=True, null=True)
    num_questions = models.IntegerField(default=0)

    def __str__(self):
        return f"Project {self.pk}: {self.name} User: {self.user} Pw required: {self.pw_requirement}"

class Question(models.Model):
    # question_type should be: "Open-ended Question", "Question and Answer", or "Multiple Choice"
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="inquirer")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="pjk_question")
    question = models.CharField(max_length=150)
    question_type = models.CharField(max_length=50)
    answer = models.CharField(max_length=150, blank=True, null=True)
    nr_choices = models.IntegerField(default=0)
    option1 = models.CharField(max_length=150, blank=True, null=True)
    option2 = models.CharField(max_length=150, blank=True, null=True)
    option3 = models.CharField(max_length=150, blank=True, null=True)
    option4 = models.CharField(max_length=150, blank=True, null=True)
    option5 = models.CharField(max_length=150, blank=True, null=True)
    correctOptionEnabled = models.BooleanField(blank=True, null=True, default=False)
    correctOption = models.IntegerField(default=0)
    position = models.IntegerField(default=1)

    def __str__(self):
        return f"Question {self.pk}: {self.question_type} User: {self.user} Project: {self.project}"
