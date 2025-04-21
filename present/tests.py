"""
Test cases for present.
To run tests in the terminal, run: 
`python manage.py test present.tests`
"""
from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project, Question, Answer, Respondent
from website.models import User

class PresentIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="presenter", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Live Project", prj_code="XYZ789")
        self.question1 = Question.objects.create(user=self.user, project=self.project, question="Q1?", position=1)
        self.question2 = Question.objects.create(user=self.user, project=self.project, question="Q2?", position=2)
        self.url = reverse("present:index", args=[self.project.prj_code])

    def test_present_index_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "present/index.html")
        self.assertIn("project", response.context)
        self.assertIn("questions", response.context)
        self.assertEqual(response.context["num_questions"], 2)
        self.assertContains(response, "Q1?")
        self.assertContains(response, "Q2?")

class LiveVoteCountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="voteuser", password="testpass")
        self.project = Project.objects.create(
            user=self.user,
            name="Voting Project",
            num_respondents=42
        )
        self.url = reverse("present:live_vote_count", args=[self.project.pk])

    def test_live_vote_count_returns_correct_number(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"vote_count": 42})

    def test_live_vote_count_invalid_project_id(self):
        url = reverse("present:live_vote_count", args=[9999])  # non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class DeliverAnswersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="presenter", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Delivery Project", poll_nr=1)
        
        # Create a respondent so the answer has a valid foreign key
        self.respondent = Respondent.objects.create(username="Test Respondent")

        self.question = Question.objects.create(
            user=self.user,
            project=self.project,
            question="What's the capital of France?",
            position=1
        )
        self.answer = Answer.objects.create(
            user=self.respondent,
            project=self.project,
            question=self.question,
            users_answer="Paris",
            users_choice=0,
            is_correct=1,
            poll_batch=1
        )
        self.url = reverse("present:deliver_answers", kwargs={"id": self.project.pk})

    def test_deliver_answers_valid_project(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("questions", data)
        self.assertIn("answers", data)
        self.assertIn("Paris", data["answers"])

    def test_deliver_answers_invalid_project(self):
        invalid_url = reverse("present:deliver_answers", kwargs={"id": 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)  # Correctly expecting 404