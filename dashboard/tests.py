"""
Test cases for dashboard.
To run tests in the terminal, run: 
`python manage.py test dashboard.tests`
"""
import os
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from dashboard.models import Project, Question, Answer, Result
from website.models import User
from dashboard.utils import qr_code_generator

# Index
class DashboardIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("dashboard:index")

    def test_index_redirects_if_not_logged_in(self): # page redirects if not logged in (302 is redirect code)
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200) 

    def test_index_loads_for_logged_in_user(self): # correct page loads if logged in
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")

    def test_index_with_project(self): # user can log in and see projects
        self.client.login(username="testuser", password="testpass")
        Project.objects.create(user=self.user, name="Test Project")
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context["projects"])

# Add projects
class AddProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse("dashboard:add_project")
        self.dashboard_url = reverse("dashboard:index")

    def test_add_project_redirects_if_not_logged_in(self):
        response = self.client.post(self.url, data={})
        self.assertNotEqual(response.status_code, 200)

    def test_add_project_successfully(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "projectname": "Test Project",
            "usernamenabled": "on",
            "answernabled": "on"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.name, "Test Project")
        self.assertTrue(project.username_requirement)
        self.assertTrue(project.show_answers)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={'id': project.pk}))

    def test_add_project_missing_password(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "projectname": "Secure Project",
            "pwenabled": "on",  # password enabled but missing value
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(Project.objects.count(), 0)
        self.assertContains(response, "No password set: project could not be saved.")

    def test_add_project_with_password(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "projectname": "Secure Project",
            "pwenabled": "on",
            "projectpw": "secret123"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertTrue(project.pw_requirement)
        self.assertEqual(project.pw, "secret123")
        self.assertRedirects(response, reverse("dashboard:project", kwargs={'id': project.pk}))

class ProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Test Project", num_questions=0)
        self.url = reverse("dashboard:project", kwargs={"id": self.project.pk})
        self.client.login(username="testuser", password="testpass")

    def test_project_view_success_no_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/project.html")
        self.assertEqual(response.context["project"], self.project)
        self.assertIsNone(response.context["questions"])

    def test_project_view_success_with_questions(self):
        q1 = Question.objects.create(user=self.user, project=self.project, question="What is 2+2?",
                                     question_type="Open-ended Question", position=1)
        self.project.num_questions = 1
        self.project.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(q1, response.context["questions"])

    def test_project_view_invalid_project(self):
        invalid_url = reverse("dashboard:project", kwargs={"id": 9999})
        response = self.client.get(invalid_url, follow=False)  # Don't follow redirect
        self.assertEqual(response.status_code, 302)  # Should redirect
        # Now check the session
        session = self.client.session
        self.assertEqual(session["index_message"], "There was an error opening your project, please try again.")

class OpenPollViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Poll Project", is_live=False)
        self.url = reverse("dashboard:open_poll", kwargs={"id": self.project.pk})

    def test_open_poll_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertTrue(self.project.is_live)
        self.assertEqual(response.json()["status"], "success")

    def test_open_poll_invalid_project(self):
        invalid_url = reverse("dashboard:open_poll", kwargs={"id": 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "failure")

class ClosePollViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(
            user=self.user,
            name="Poll Project",
            is_live=True,
            num_respondents=1
        )
        self.url = reverse("dashboard:close_poll", kwargs={"id": self.project.pk})

    def test_close_poll_success_no_answers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertFalse(self.project.is_live)
        self.assertEqual(Result.objects.count(), 0)
        self.assertEqual(response.json()["status"], "success")

    def test_close_poll_success_with_answers_and_no_result_yet(self):
        # Create a question
        question = Question.objects.create(
            user=self.user,
            project=self.project,
            question="Test Q?",
            question_type="Question and Answer",
            answer="42",
            position=1
        )

        # Create a respondent 
        from dashboard.models import Respondent
        respondent = Respondent.objects.create(username="anon123")

        # Create an answer by that respondent
        Answer.objects.create(
            user=respondent,  
            project=self.project,
            question=question,
            users_answer="42",
            users_choice=0,
            is_correct=1,
            poll_batch=self.project.poll_nr
        )

        # Perform the request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertFalse(self.project.is_live)
        self.assertEqual(Result.objects.count(), 1)
        self.assertEqual(response.json()["status"], "success")

    def test_close_poll_with_invalid_project(self):
        invalid_url = reverse("dashboard:close_poll", kwargs={"id": 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "failure")

from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project
from website.models import User

class EditProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Initial Project")
        self.url = reverse("dashboard:edit_project", kwargs={"id": self.project.pk})
        self.project_url = reverse("dashboard:project", kwargs={"id": self.project.pk})
        self.index_url = reverse("dashboard:index")
        self.client.login(username="testuser", password="testpass")

    def test_get_project_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("project", response.json())

    def test_edit_project_success(self):
        data = {
            "projectname": "Updated Project",
            "usernamenabled": "on",
            "pwenabled": "on",
            "projectpw": "newpass",
            "answernabled": "on"
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, self.project_url)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")
        self.assertTrue(self.project.username_requirement)
        self.assertTrue(self.project.pw_requirement)
        self.assertEqual(self.project.pw, "newpass")
        self.assertTrue(self.project.show_answers)

    def test_edit_project_missing_password(self):
        self.client.login(username="testuser", password="testpass")
        data = {
            "projectname": "Should Fail",
            "pwenabled": "on"  # checkbox is on, but password not provided
        }
        response = self.client.post(self.url, data, follow=True)

        # Look for the actual HTML output of the message
        self.assertContains(response, "No password set, project could not be saved.")

    def test_edit_project_invalid_id(self):
        self.client.login(username="testuser", password="testpass")
        invalid_url = reverse("dashboard:edit_project", kwargs={"id": 999})  # non-existent
        data = {
            "projectname": "Should Fail"
        }
        response = self.client.post(invalid_url, data, follow=True)

        self.assertContains(response, "There was an error editing your project.")

class DeleteProjectViewTest(TestCase):
    # Expect following in terminal: Failed to delete QR code image: [WinError 2] The system cannot find the file specified
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Project To Delete")
        self.url = reverse("dashboard:delete_project", kwargs={"id": self.project.pk})
        self.index_url = reverse("dashboard:index")

    def test_delete_project_success(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, self.index_url)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertContains(response, "Project deleted successfully!")

    def test_delete_project_invalid_id(self):
        self.client.login(username="testuser", password="testpass")
        invalid_url = reverse("dashboard:delete_project", kwargs={"id": 999})
        response = self.client.get(invalid_url, follow=True)

        self.assertRedirects(response, self.index_url)
        self.assertContains(response, "There was an error deleting your project, please try again.")

class AddQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.project = Project.objects.create(user=self.user, name="Test Project")
        self.url = reverse("dashboard:add_question")

    def test_add_open_ended_question_success(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "What's your opinion on AI?",
            "question": "on",  # Open-ended
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={"id": self.project.pk}))
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_type, "Open-ended Question")

    def test_add_question_missing_type(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "What do you think?",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={"id": self.project.pk}))
        self.assertEqual(Question.objects.count(), 0)

    def test_add_multiple_choice_question_with_answer(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "What is 2 + 2?",
            "multiplechoice": "on",
            "nrchoices": "4",
            "choice1": "1",
            "choice2": "2",
            "choice3": "4",
            "choice4": "5",
            "choiceAnswerEnabled": "on",
            "rightChoice": "3"
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={"id": self.project.pk}))
        self.assertEqual(Question.objects.count(), 1)
        q = Question.objects.first()
        self.assertEqual(q.correctOption, 3) 
        self.assertEqual(q.option3, "4")
        self.assertEqual(q.question_type, "Multiple Choice")
        self.assertTrue(q.correctOptionEnabled)

    def test_add_qanda_question(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "Capital of France?",
            "qanda": "on",
            "theanswer": "Paris"
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={"id": self.project.pk}))
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_type, "Question and Answer")
        self.assertEqual(question.answer, "Paris")

class QuestionOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.project = Project.objects.create(user=self.user, name="Test Project")
        # Create sample questions
        self.questions = [
            Question.objects.create(user=self.user, project=self.project, question=f"Q{i}", position=i)
            for i in range(1, 5)
        ]
        self.url = reverse("dashboard:question_order")  # update this if your URL name is different

    def test_question_order_successful(self):
        new_order = [[q.pk, i] for i, q in enumerate(reversed(self.questions))]
        response = self.client.post(self.url, data=json.dumps({'body': new_order}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Question order saved successfully')
        # Check updated order in DB
        for i, qdata in enumerate(new_order):
            q = Question.objects.get(pk=qdata[0])
            self.assertEqual(q.position, qdata[1] + 1)

    def test_question_order_with_invalid_question(self):
        invalid_order = [[999, 0]]
        response = self.client.post(self.url, data=json.dumps({'body': invalid_order}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('might not exist', response.json()['message'])

    def test_question_order_with_invalid_data_format(self):
        bad_data = {'body': [[1]]}  # Missing position
        response = self.client.post(self.url, data=json.dumps(bad_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Invalid data format')

    def test_question_order_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Oops, there was an error with the question ordering.')

from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project, Question
from website.models import User
import json

class EditQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.project = Project.objects.create(user=self.user, name="Test Project")
        self.question = Question.objects.create(
            user=self.user,
            project=self.project,
            question="Original Question",
            question_type="Open-ended Question",
            position=1
        )
        self.url = reverse("dashboard:edit_question", kwargs={"id": self.question.pk})

    def test_edit_question_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("question", data)
        self.assertIn("Original Question", data["question"])

    def test_edit_question_post_open_ended(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "Updated Question",
            "question": "on",  # triggers open-ended type
            "choice1": "", "choice2": "", "choice3": "", "choice4": "", "choice5": ""
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={'id': self.project.pk}))
        updated_question = Question.objects.get(pk=self.question.pk)
        self.assertEqual(updated_question.question, "Updated Question")
        self.assertEqual(updated_question.question_type, "Open-ended Question")

    def test_edit_question_post_qanda(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "Q&A Question",
            "qanda": "on",
            "theanswer": "42",
            "choice1": "", "choice2": "", "choice3": "", "choice4": "", "choice5": ""
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={'id': self.project.pk}))
        updated = Question.objects.get(pk=self.question.pk)
        self.assertEqual(updated.question_type, "Question and Answer")
        self.assertEqual(updated.answer, "42")

    def test_edit_question_post_multiple_choice_with_answer(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "MC Question",
            "multiplechoice": "on",
            "nrchoices": 3,
            "choiceAnswerEnabled": "on",
            "rightChoice": "2",
            "choice1": "Option 1",
            "choice2": "Option 2",
            "choice3": "Option 3",
            "choice4": "",
            "choice5": ""
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:project", kwargs={'id': self.project.pk}))
        q = Question.objects.get(pk=self.question.pk)
        self.assertEqual(q.question_type, "Multiple Choice")
        self.assertEqual(q.correctOptionEnabled, True)
        self.assertEqual(q.correctOption, 2)
        self.assertEqual(q.option2, "Option 2")

    def test_edit_question_missing_type(self):
        data = {
            "project_pk": self.project.pk,
            "thequestion": "No Type",
            "choice1": "", "choice2": "", "choice3": "", "choice4": "", "choice5": ""
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertContains(response, "There was a problem editing your question. Select a question type.")

class DeleteQuestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

        self.project = Project.objects.create(user=self.user, name="Project", num_questions=2)
        self.q1 = Question.objects.create(
            user=self.user, project=self.project, question="First?", question_type="Open-ended Question", position=1
        )
        self.q2 = Question.objects.create(
            user=self.user, project=self.project, question="Second?", question_type="Open-ended Question", position=2
        )

    def test_delete_question_successfully(self):
        url = reverse("dashboard:delete_question", kwargs={"id": self.q1.pk})
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse("dashboard:project", kwargs={"id": self.project.pk}))
        self.assertFalse(Question.objects.filter(pk=self.q1.pk).exists())

        # q2 should now be at position 1
        q2 = Question.objects.get(pk=self.q2.pk)
        self.assertEqual(q2.position, 1)

        # project should have 1 question now
        project = Project.objects.get(pk=self.project.pk)
        self.assertEqual(project.num_questions, 1)

        self.assertContains(response, "Question deleted successfully!")

    def test_delete_question_invalid_id(self):
        url = reverse("dashboard:delete_question", kwargs={"id": 9999})  # non-existing question ID
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse("dashboard:index"))
        self.assertContains(response, "There was a problem deleting your question. Please try again")

from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project, Question, Respondent, Answer, Result
from website.models import User
import json

class ProjectAnswersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_login(self.user)
        self.project = Project.objects.create(user=self.user, name="Test Project", poll_nr=1)

        # Create a Respondent
        self.respondent = Respondent.objects.create(username="Alice")

        # Create a Question
        self.question = Question.objects.create(
            user=self.user,
            project=self.project,
            question="What is 2+2?",
            question_type="Question and Answer",
            answer="4",
            position=1,
            correctOptionEnabled=True,
            correctOption=1
        )

        # Create an Answer
        Answer.objects.create(
            user=self.respondent,
            project=self.project,
            question=self.question,
            users_answer="4",
            is_correct=1,
            users_choice=1,
            poll_batch=1
        )

        # Create a Result
        self.result = Result.objects.create(
            project=self.project,
            num_respondents=1,
            poll_batch=1,
            question_list_object=json.dumps([{
                "question_pk": self.question.pk,
                "question": self.question.question,
                "question_type": self.question.question_type,
                "question_num_choices": self.question.nr_choices,
                "question_options": [self.question.option1, self.question.option2, self.question.option3, self.question.option4, self.question.option5],
                "question_options_chosen_total": [1, 0, 0, 0, 0],
                "total_answers": 1,
                "question_has_answer": True,
                "total_correct_ans": 1,
                "percentage_ans_that_are_correct": "100%"
            }])
        )

    def test_project_answers_view_renders_correctly(self):
        url = reverse("dashboard:project_answers", kwargs={"id": self.project.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/project_answers.html")
        self.assertContains(response, self.project.name)
        self.assertContains(response, "What is 2+2?")
        self.assertEqual(response.context["project"], self.project)
        self.assertEqual(response.context["results"], self.result)
        self.assertIn("question_results", response.context)
        self.assertIn("respondents", response.context)

class SetSessionMessageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("dashboard:set_session_message")  # use your actual route name

    def test_sets_message_successfully(self):
        response = self.client.post(self.url, data={"message": "Hello world"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
        self.assertEqual(self.client.session["index_message"], "Hello world")

    def test_returns_error_when_message_missing(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"status": "error"})

    def test_get_method_returns_error(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"status": "error"})

class QRCodeViewTest(TestCase):

    def setUp(self):
        self.project_code = "TESTQR123"
        self.qr_filename = f"qr_{self.project_code}.png"
        self.qr_path = os.path.join(settings.MEDIA_ROOT, "qr_codes", self.qr_filename)

        # Clean up any old test QR code file
        if os.path.exists(self.qr_path):
            os.remove(self.qr_path)

    def tearDown(self):
        # Clean up generated QR code after test
        if os.path.exists(self.qr_path):
            os.remove(self.qr_path)

    def test_qr_code_is_generated_and_redirects(self):
        """Should generate a QR code and redirect to the media file URL"""
        url = reverse("dashboard:qr_code", args=[self.project_code])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  # Redirect
        expected_url = f"{settings.MEDIA_URL}qr_codes/{self.qr_filename}"
        self.assertEqual(response.url, expected_url)

        # Confirm file was created
        self.assertTrue(os.path.exists(self.qr_path))

    def test_qr_code_redirects_if_already_exists(self):
        """Should redirect to existing QR code without regenerating"""
        # Generate first
        qr_code_generator(self.project_code)

        # Now call view
        url = reverse("dashboard:qr_code", args=[self.project_code])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{settings.MEDIA_URL}qr_codes/{self.qr_filename}")
        self.assertTrue(os.path.exists(self.qr_path))

    def test_qr_code_view_handles_failure(self):
        """Simulate QR code generation failure (by mocking)"""
        from unittest.mock import patch

        with patch("dashboard.views.qr_code_generator", return_value=None):
            url = reverse("dashboard:qr_code", args=[self.project_code])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)