from django.shortcuts import render
from dashboard.models import Project, Question

# Create your views here.

def index(request, prj):
    # Query projects for project code (prj)
    the_project = Project.objects.get(prj_code=prj)
    # Check if project is being presented
    # if project is being presented:
    if the_project.is_live:
        # Get questions that belong to the project
        the_questions = Question.objects.filter(
            project=the_project).order_by("position")
        print("project is live!")
        # Send project and questions to index
        return render(request, "poll/index.html")
    # else if project not being presented return error page
        #place error page in the website app


# Create function that saves the answers and sends json to update number of votes
# If presentor is showing the results, show error page if person is still trying to cast a vote.
