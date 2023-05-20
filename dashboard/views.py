from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from website.models import User
from dashboard.models import Project, Question
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

# index is the user's dashboard
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


def project(request, id, message=None):
    # print(id)
    # the_project = Project.objects.get(pk=id)
    # print(the_project)
    # print(the_project.id)
    # print(the_project.name)
    # return render(request, "dashboard/project.html", {
    #     "project": the_project,
    #     "message": message
    # })
    try:
        the_project = Project.objects.get(pk=id)
        if the_project.num_questions > 0:
            the_questions = Question.objects.filter(
                project=the_project).order_by("position")
        else:
            the_questions = None
        return render(request, "dashboard/project.html", {
            "project": the_project,
            "questions": the_questions,
            "message": message
        })
    except:
        return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "There was an error opening your project, please try again."
                }))          

def delete_project(request, id):
    try:
        the_project = Project.objects.get(pk=id)
        the_project.delete()
        return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "Project deleted successfully!"}))
    except:
        return HttpResponseRedirect(reverse("dashboard:index", kwargs={'message': "There was an error deleting your project, please try again."}))

def add_question(request):
    if request.method == "POST":
        the_user = User.objects.get(pk=request.user.pk)
        the_project = Project.objects.get(pk=int(request.POST['project_pk']))
        the_question = request.POST['thequestion']
        if 'question' in request.POST:
            the_question_type = "Open-ended Question"
            the_nr_choices = 0
        elif 'qanda' in request.POST:
            the_question_type = "Question and Answer"
            the_nr_choices = 0
        elif 'multiplechoice' in request.POST:
            the_question_type = "Multiple Choice"
            the_nr_choices = request.POST['nrchoices']
        else:
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk, 'message': "There was a problem adding your question. Select a question type."
                }))
        if 'the_answer' in request.POST:
            the_answer = request.POST['theanswer']
        else:
            the_answer = ""
        if 'choiceAnswerEnabled' in request.POST:
            correct_option_enabled = True
            the_correct_choice = request.POST['rightChoice']
        else:
            correct_option_enabled = False
            the_correct_choice = 1
        the_1_option = request.POST['choice1']
        the_2_option = request.POST['choice2']
        the_3_option = request.POST['choice3']
        the_4_option = request.POST['choice4']
        the_5_option = request.POST['choice5']

        the_position = the_project.num_questions + 1

        try:
            new_q = Question(
                user=the_user, project=the_project, question=the_question, question_type=the_question_type,
                answer=the_answer, nr_choices=the_nr_choices, option1=the_1_option, option2=the_2_option,
                option3=the_3_option, option4=the_4_option, option5=the_5_option, correctOptionEnabled=correct_option_enabled,
                correctOption=the_correct_choice, position=the_position
            )
            new_q.save()
            the_project.num_questions = the_position
            the_project.save()
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
        except:
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={
                'id': the_project.pk, 
                'message': "There was a problem adding your question. Please try again"
                }))

# question_order gets data from JS getOrderOfQuestions() function and saves the new question position
# Sample json data: {'body': [[1, 0], [2, 1], [3, 2], [4, 3]]}
# Each inner array contains: the question's pk and it's new position. Question order might be important for the user.
@csrf_exempt
def question_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get('body', [])

        for question_data in body:
            if len(question_data) == 2:
                question_pk, position = question_data
                try:
                    question = Question.objects.get(pk=question_pk)
                    question.position = position
                    question.save()
                except Question.DoesNotExist:
                    response_data = {
                        'message': 'There was an issue, a question might not exist'}
                    return JsonResponse(response_data)
            else:
                response_data = {'message': 'Invalid data format'}
                return JsonResponse(response_data)

        response_data = {'message': 'Question order saved successfully'}
        return JsonResponse(response_data)

    response_data = {'message': 'Oops, there was an error with the question ordering.'}
    return JsonResponse(response_data)

# Function that sends Quention object information to JS the function editQuestionData. 
@csrf_exempt
def edit_question(request, id):
    question = Question.objects.get(pk=id)
    serialized_question = serialize('json', [question])
    return JsonResponse({'question': serialized_question})
# Sample data being sent from edit_question:
# [
#     {
#         "model": "dashboard.question",
#         "pk": 1,
#         "fields": {
#             "user": 2,
#             "project": 4,
#             "question": "How are you today",
#             "question_type": "Open-ended Question",
#             "answer": null,
#             "nr_choices": 0,
#             "option1": null,
#             "option2": null,
#             "option3": null,
#             "option4": null,
#             "option5": null,
#             "correctOptionEnabled": false,
#             "correctOption": 1,
#             "position": 0
#         }
#     }
# ]

# def delete_question(request):
#     return

# def edit_project(request):
#     return