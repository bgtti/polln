from django.shortcuts import render
from dashboard.models import Project, Question

# Create your views here.

def index(request, prj):
    # Query projects for project code (prj)
    the_project = Project.objects.get(prj_code=prj)
    # Set project's presentation status to true if it already isnt
    # Generate QR code
    # Send this project to index
    return render(request, "present/index.html")

# Create function that gets all answers and displays them
# When displaying answers, set presentation status to false to stop further vote count