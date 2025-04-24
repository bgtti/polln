"""
Test cases for website.
To run tests in the terminal, run: 
`python manage.py test website.tests`
"""
from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project
from website.models import User

class WebsiteIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("website:index")

    def test_index_view_no_message(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/index.html")
        self.assertIsNone(response.context["message"])

    def test_index_view_with_message(self):
        session = self.client.session
        session["home_message"] = "Welcome back!"
        session.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back!")
        self.assertIsNone(self.client.session.get("home_message"))

class WebsiteGuideViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("website:guide")

    def test_guide_view_renders_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/guide.html")

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("website:login")  
        self.dashboard_url = reverse("dashboard:index")

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/login.html")

    def test_login_view_post_valid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpass"
        })
        self.assertRedirects(response, self.dashboard_url)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/login.html")
        self.assertContains(response, "Invalid username and/or password.")

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="logoutuser", password="logoutpass")
        self.login_url = reverse("website:login")
        self.logout_url = reverse("website:logout")  # adjust if your URL name is different
        self.index_url = reverse("website:index")

    def test_logout_view(self):
        # Log the user in
        self.client.login(username="logoutuser", password="logoutpass")

        # Ensure user is authenticated
        response = self.client.get(self.index_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Call the logout view
        response = self.client.get(self.logout_url)

        # Ensure redirection to homepage
        self.assertRedirects(response, self.index_url)

        # Ensure user is logged out
        response = self.client.get(self.index_url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("website:signup")  # make sure your URL name matches

    def test_signup_page_renders_on_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/signup.html")

    def test_successful_signup(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
            "confirmation": "securepass123"
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("dashboard:index"))

        # Check user was created and is authenticated
        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

    def test_password_mismatch(self):
        data = {
            "username": "anotheruser",
            "email": "another@example.com",
            "password": "pass1",
            "confirmation": "pass2"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords must match.")

    def test_username_already_taken(self):
        User.objects.create_user(username="duplicateuser", email="existing@example.com", password="somepass")
        data = {
            "username": "duplicateuser",
            "email": "new@example.com",
            "password": "securepass",
            "confirmation": "securepass"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already taken.")

class DeleteAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="deleteuser", password="testpass")
        self.client.login(username="deleteuser", password="testpass")
        self.url = reverse("website:delete_account")

        # Create a project tied to the user
        self.project = Project.objects.create(
            user=self.user,
            name="Project to delete",
            prj_code="DEL123"
        )

    def test_delete_account_success(self):
        response = self.client.post(self.url, follow=True)

        # Check user is deleted
        self.assertFalse(User.objects.filter(username="deleteuser").exists())
        self.assertFalse(Project.objects.filter(prj_code="DEL123").exists())

        # Check redirect and success message (from session → context → HTML)
        self.assertRedirects(response, reverse("website:index"))
        self.assertContains(response, "Account deleted successfully!")

    def test_delete_account_requires_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_delete_account_requires_login(self):
        self.client.logout()
        response = self.client.post(self.url)
        login_url = reverse("website:login")
        expected_redirect = f"{login_url}/?next={self.url}"
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect)