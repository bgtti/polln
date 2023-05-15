from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "dashboard/index.html")

def add_project(request):
    if request.method == "POST":
        # Add project when button is clicked: i dont need js, a page reload would be fine
        return HttpResponseRedirect(reverse("dashboard:index"))
