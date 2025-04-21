"""
Test cases for poll.
To run tests in the terminal, run: 
`python manage.py test poll.tests`
"""
from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project, Question, Answer, Respondent
from website.models import User
import json

class PollIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            user=self.user,
            name="Test Project",
            prj_code="ABC123"
        )
        self.url = reverse("poll:index", args=["ABC123"])
        self.invalid_url = reverse("poll:index", args=["WRONG01"])

    def test_index_view_valid_project_code(self):
        Question.objects.create(
            project=self.project,
            user=self.user,
            question="What is your name?",
            position=1
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "poll/index.html")
        self.assertIn("project", response.context)
        self.assertIn("questions", response.context)
        self.assertEqual(response.context["num_questions"], 1)

    def test_index_view_invalid_project_code_redirects(self):
        response = self.client.get(self.invalid_url, follow=True)

        self.assertRedirects(response, reverse("website:index"))
        self.assertContains(response, "Code not valid. Check the six-digit project code and try again.")

class CheckIfPollOpenViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            user=self.user,  # Assign user to avoid IntegrityError
            name="Poll Project",
            is_live=True
        )

    def test_poll_is_open(self):
        url = reverse("poll:check_if_poll_open")
        response = self.client.post(
            url,
            json.dumps({"project": self.project.pk}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})

    def test_poll_is_closed(self):
        self.project.is_live = False
        self.project.save()

        url = reverse("poll:check_if_poll_open")
        response = self.client.post(
            url,
            json.dumps({"project": self.project.pk}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Poll is closed"})

    def test_invalid_project_id(self):
        url = reverse("poll:check_if_poll_open")
        response = self.client.post(
            url,
            json.dumps({"project": None}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Invalid Id"})

class GetAnswersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Poll Project")
        self.question_oe = Question.objects.create(
            user=self.user, project=self.project, question="How are you?", question_type="Open-ended Question", position=1
        )
        self.question_qa = Question.objects.create(
            user=self.user, project=self.project, question="Say Hello", question_type="Question and Answer", answer="hello", position=2
        )
        self.question_mc = Question.objects.create(
            user=self.user, project=self.project, question="Pick one", question_type="Multiple Choice",
            correctOptionEnabled=True, correctOption=3, position=3
        )
        self.url = reverse("poll:get_answers")

    def test_get_answers_success(self):
        data = {
            "project": self.project.pk,
            "username": "Bruna",
            "answers": [
                {"question": self.question_oe.pk, "answer": "good", "type": "OE"},
                {"question": self.question_qa.pk, "answer": "hello", "type": "QA"},
                {"question": self.question_mc.pk, "answer": "option3", "type": "MC"},
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})
        self.assertEqual(Respondent.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 3)
        self.project.refresh_from_db()
        self.assertEqual(self.project.num_respondents, 1)

    def test_get_answers_invalid_data(self):
        response = self.client.post(self.url, json.dumps({"project": None, "answers": []}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Invalid data"})
        self.assertEqual(Respondent.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)

    def test_get_answers_invalid_question_type(self):
        data = {
            "project": self.project.pk,
            "answers": [
                {"question": self.question_oe.pk, "answer": "something", "type": "INVALID"}
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Invalid type"})

class CheckPollPasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            user=self.user,
            name="Password Protected Project",
            pw="secure123"
        )
        self.url = reverse("poll:check_poll_password")

    def test_correct_password(self):
        data = {
            "project": self.project.pk,
            "password": "secure123"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})

    def test_incorrect_password(self):
        data = {
            "project": self.project.pk,
            "password": "wrongpass"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Wrong password"})

    def test_invalid_project_id(self):
        data = {
            "project": None,
            "password": "doesntmatter"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "error", "message": "Invalid Id"})