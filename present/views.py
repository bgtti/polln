from django.shortcuts import render
from dashboard.models import Project, Question

# Create your views here.

def index(request, prj):
    # Query projects for project code (prj)
    # print(type(prj))
    # d = Project.objects.get(pk=4)
    # print(type(d.prj_code))
    # print(type(d.prj_code) == type(prj))

    # g = Project.objects.filter(prj_code=prj)[0]
    # print(g)
    the_project = Project.objects.get(prj_code=prj)
    print(the_project)
    # Set project's presentation status to true if it already isnt
    # Generate QR code
    # Send this project to index
    return render(request, "present/index.html", {
        "project": the_project,
    })

# Create function that gets all answers and displays them
# When displaying answers, set presentation status to false to stop further vote count