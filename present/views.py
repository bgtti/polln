from django.shortcuts import render
from dashboard.models import Project, Question
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Present project

def index(request, prj):
    the_project = Project.objects.get(prj_code=prj)
    the_questions = Question.objects.filter(project=the_project)

    return render(request, "present/index.html", {
        "project": the_project,
        "questions": the_questions,
        "num_questions": len(the_questions)
    })

# Send number of respondents who have casted their votes
# This information is requested in time intervals and will be shown on the user's presentation
@csrf_exempt
def live_vote_count(request, id):
    if request.method == 'GET':
        the_project = Project.objects.get(pk=id)
        num_votes = the_project.num_respondents
        data = {
            'vote_count': num_votes
        }

        return JsonResponse(data)
