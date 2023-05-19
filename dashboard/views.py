from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from website.models import User
from dashboard.models import Project

# Create your views here.

def index(request, message=None):
    user = User.objects.get(pk=request.user.pk)
    projects = Project.objects.filter(user=user).order_by("pk").reverse()
    if not projects:
        projects = None
    return render(request, "dashboard/index.html", {
        "projects": projects,
        "message": message
    })

def add_project(request):
    if request.method == "POST":
        print("I AM HERE")
        pjt_name = request.POST['projectname']
        user = User.objects.get(pk=request.user.pk)
        if 'pwenabled' in request.POST:
            set_pw = True
            pw = request.POST['projectpw']
            if not pw or pw == "":
                return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "No password set, project could not be saved."
                }))
        else:
            set_pw = False
            pw=""
        try: 
            new_pjt = Project(user=user, name=pjt_name,  pw_requirement=set_pw, pw=pw)
            new_pjt.save()
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': new_pjt.pk}))
        except:
            return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "There was an error saving your project, please try again."
                }))

def project(request, id):
    print(id)
    the_project = Project.objects.get(pk=id)
    print(the_project)
    print(the_project.id)
    print(the_project.name)
    return render(request, "dashboard/project.html", {
        "project": the_project,
    })
    # try:
    #     print(id)
    #     the_project = Project.objects.get(pk=id)
    #     print(the_project)
    #     print(the_project.id)
    #     print(the_project.name)
    #     return render(request, "dashboard/project.html", {
    #         "project": the_project,
    #     })
    # except:
    #     print("problem")
    #     return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "There was an error opening your project, please try again."
    #             }))          
    

def delete_project(request, id):
    try:
        the_project = Project.objects.get(pk=id)
        the_project.delete()
        return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "Project deleted successfully!"}))
    except:
        return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "There was an error deleting your project, please try again."}))

def add_question(request):
    return