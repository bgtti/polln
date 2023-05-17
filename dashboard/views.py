from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from website.models import User
from dashboard.models import Project

# Create your views here.

def index(request):
    user = User.objects.get(pk=request.user.pk)
    projects = Project.objects.filter(user=user).order_by("pk").reverse()
    if not projects:
        projects = None
    return render(request, "dashboard/index.html", {
        "projects": projects,
    })

def add_project(request):
    if request.method == "POST":
        pjt_name = request.POST['projectname']
        user = User.objects.get(pk=request.user.pk)
        if 'pwenabled' in request.POST:
            set_pw = True
            pw = request.POST['projectpw']
            if not pw or pw == "":
                return HttpResponseRedirect(reverse("dashboard:index", {
                    "message":"No password set, project could not be saved."
                }))
        else:
            set_pw = False
            pw=""

        try: 
            new_pjt = Project(user=user, name=pjt_name,  pw_requirement=set_pw, pw=pw)
            new_pjt.save()
            return HttpResponseRedirect(reverse("dashboard:index"))
        except:
            return HttpResponseRedirect(reverse("dashboard:index", {
                "message": "There was an error saving your project, please try again."
            }))

