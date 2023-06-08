from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from dashboard.models import Project, Question, Respondent, Answer
from dashboard.utils import compareTwoStrings
import json

def index(request, prj):
    # Remove trailing spaces from the user's input before proceeding
    prj = prj.strip()
    try:
        # Query projects for project code (prj)
        the_project = Project.objects.get(prj_code=prj)

        # Get questions that belong to the project
        the_questions = Question.objects.filter(
            project=the_project).order_by("position")
        return render(request, "poll/index.html", {
            "project": the_project,
            "questions": the_questions,
            "num_questions": len(the_questions)
        })
    except:
        request.session['home_message'] = "Code not valid. Check the six-digit project code and try again."
        return HttpResponseRedirect(reverse("website:index"))

# checks if poll is open and sends information to JS function to decide if answers can be submitted
@csrf_exempt
def check_if_poll_open(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id = int(data.get('project'))
        if project_id:
            the_project = Project.objects.get(pk=project_id)
            poll_is_open = the_project.is_live
            if poll_is_open:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Poll is closed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Id'})

# get_answers function: get the answer sent by JS function submitPollAnswers and save to db
# Sample data being received:
# {
#     "project": "14",
#     "answers": [
#         {
#             "question": "15",
#             "answer": "good",
#             "type": "OE"
#         },
#         {
#             "question": "16",
#             "answer": "hello",
#             "type": "QA"
#         },
#         {
#             "question": "17",
#             "answer": "option3",
#             "type": "MC"
#         }
#     ]
# }
@csrf_exempt
def get_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id = int(data.get('project'))
        answers = data.get('answers')
        username = data.get('username')
        if project_id and answers:
            the_project = Project.objects.get(pk=project_id)
            # Create a new Respondent object
            the_username = "anonymous"
            if username:
                the_username = username
            new_respondent = Respondent(username=the_username)
            new_respondent.save()
            # Iterate over the received answers and create new Answer objects
            for answer_data in answers:
                question_id = int(answer_data.get('question'))
                answer_text = answer_data.get('answer')
                question_type = answer_data.get('type')

                if question_id and answer_text and question_type:
                    # Get Question
                    the_question = Question.objects.get(pk=question_id)
                    choice = 0
                    correctness = 0
                    if question_type == "OE":
                        correctness = 0
                    elif question_type == "QA":
                        if compareTwoStrings(the_question.answer, answer_text):
                            correctness = 1
                        else:
                            correctness = 2
                    elif question_type == "MC":
                        choice = int(answer_text[-1])
                        if the_question.correctOptionEnabled:
                            if choice == the_question.correctOption:
                                correctness = 1
                            else:
                                correctness = 2
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid type'})
                    # Create a new Answer object
                    new_answer = Answer(
                        user=new_respondent,
                        project=the_project,
                        question=the_question,
                        users_answer=answer_text,
                        users_choice=choice,
                        is_correct=correctness
                    )
                    new_answer.save()
            # Update number of respondents on project
            the_project.num_respondents = the_project.num_respondents + 1 
            the_project.save()

            return JsonResponse({'status': 'success'})
        else:
            print("invalid data")
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        

def check_poll_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id = int(data.get('project'))
        project_password = data.get('password')
        if project_id:
            the_project = Project.objects.get(pk=project_id)
            if the_project.pw == project_password:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Wrong password'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Id'})
