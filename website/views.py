from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User
from dashboard.models import Project
from dashboard.utils import delete_qr_code

# If you encounter migration issues: python -m manage makemigrations
# https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory

def index(request, message=None):
    message = request.session.get('home_message')
    request.session['home_message'] = None
    return render(request, "website/index.html", {
        "message": message
    })

def guide(request):
    return render(request, "website/guide.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # return HttpResponseRedirect(reverse("index"))
            return HttpResponseRedirect(reverse("dashboard:index"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("website:index"))

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/signup.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "website/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("dashboard:index"))
    else:
        return render(request, "website/signup.html")


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        projects = Project.objects.filter(user=user)
        for project in projects:
            delete_qr_code(project.prj_code)
        user.delete()
        # Account deleted, send user to homepage with success message
        request.session['home_message'] = "Account deleted successfully!"
        return HttpResponseRedirect(reverse("website:index"))
