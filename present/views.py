from django.shortcuts import render
from dashboard.models import Project, Question, Answer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

# Present project

def index(request, prj):
    the_project = Project.objects.get(prj_code=prj)
    the_questions = Question.objects.filter(
        project=the_project).order_by("position")

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

# Send answer results

@csrf_exempt
def deliver_answers(request, id):
    if request.method == 'GET':
        the_project = Project.objects.get(pk=id)
        the_questions = Question.objects.filter(
            project=the_project)
        if the_questions.count == 1:
            serialized_questions = serialize('json', [the_questions])
        else:
            serialized_questions = serialize('json', the_questions)
        
        the_answers = Answer.objects.filter(
            project=the_project, poll_batch=the_project.poll_nr)
        serialized_answers = serialize('json', the_answers)
        
        data = {
            'questions': serialized_questions,
            'answers': serialized_answers
        }

        return JsonResponse(data)

