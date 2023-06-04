from django.db import models
from website.models import User


class Project(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=100)
    username_requirement = models.BooleanField(blank=True, null=True, default=False)
    pw_requirement = models.BooleanField(blank=True, null=True, default=False)
    pw = models.CharField(max_length=30, blank=True, null=True)
    show_answers = models.BooleanField(blank=True, null=True, default=False)
    #prj_code = user.pk + project.pk (used to generate poll url for project)
    prj_code = models.CharField(max_length=6, blank=True, null=True)
    is_live = models.BooleanField(default=False)
    #counts number of polls, representing the number of times a poll was open and received answers
    poll_nr = models.IntegerField(default=1)
    # when project is live, JS function should feed responses
    # after results are displayed, num_respondents should be zeroed again
    num_respondents = models.IntegerField(default=0)
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
        return f"Question {self.pk}: {self.question}, {self.question_type} User: {self.user} Project: {self.project}"


class Answer(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="linked_answer")
    # if user polled more than once, answers will be saved by 'batch' number, which updates according to project.poll_nr
    poll_batch = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="linked_answer")
    submission_date = models.DateTimeField(auto_now_add=True)
    # user's answer is saved. If multiple choice, the int representing the answer is saved in users_choice
    users_answer = models.CharField(max_length=150, blank=True, null=True)
    users_choice = models.IntegerField(default=0)
    # if the question was answered correctly, 1, if not, 2, if open-ended 0
    is_correct = models.IntegerField(default=0)

    # populates poll_batch every time it is saved
    def save(self, *args, **kwargs):
        self.poll_batch = self.project.poll_nr
        super().save(*args, **kwargs)


class Result(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="linked_results")
    # if user polled more than once, answers will be saved by 'batch' number, which updates according to project.poll_nr
    poll_batch = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True)
    num_respondents = models.IntegerField(default=0)
    # question list holds objects with the following info per question: 
    # question.pk, question, question_type, question_num_choices, question_options (an array from options1 to 5), 
    # question_options_chosen_total (a dict with option nr and the total votes on it),
    # total_answers,question_has_answer,total_correct_ans,percentage_ans_that_are_correct
    question_list_object = models.TextField(default="")



    # populates poll_batch every time it is saved
    def save(self, *args, **kwargs):
        self.poll_batch = self.project.poll_nr
        super().save(*args, **kwargs)
