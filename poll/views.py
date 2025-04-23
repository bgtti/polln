"""
Poll: views pertaining to poll respondents
"""
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from dashboard.models import Project, Question, Respondent, Answer
from dashboard.utils import compareTwoStrings
import json

def index(request, prj):
    """
    Returns template for respondents to answer poll questions (method = GET)
    """
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

# check if poll is open
@csrf_exempt
def check_if_poll_open(request):
    """
    Checks if poll is open and sends information to JS function to decide if answers can be submitted (method = POST)
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id = data.get('project')
        if not project_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid Id'})
        
        try:
            project_id = int(project_id)
            the_project = Project.objects.get(pk=project_id)
            if the_project.is_live:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Poll is closed'})
        except (ValueError, Project.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid Id'})

# Getting the answers
@csrf_exempt
def get_answers(request):
    """
    get the answer sent by JS function submitPollAnswers and save to db (method = POST)

    ---
    Sample data being received:
    {
        "project": "14",
        "answers": [
            {
                "question": "15",
                "answer": "good",
                "type": "OE"
            },
            {
                "question": "16",
                "answer": "hello",
                "type": "QA"
            },
            {
                "question": "17",
                "answer": "option3",
                "type": "MC"
            }
        ]
    }
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Malformed JSON'})

    project_id_raw = data.get('project')
    answers = data.get('answers')
    username = data.get('username', 'anonymous') or "anonymous" 

    if project_id_raw is None or not answers:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    try:
        project_id = int(project_id_raw)
        the_project = Project.objects.get(pk=project_id)
    except (ValueError, Project.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Invalid project ID'})

    # Create a new Respondent
    new_respondent = Respondent(username=username)
    new_respondent.save()   
    
    # Iterate over the received answers and create new Answer objects
    for answer_data in answers:
        try:
            question_id = int(answer_data.get('question'))
            answer_text = answer_data.get('answer')
            question_type = answer_data.get('type') 
            if question_id and answer_text and question_type:
                # Get question
                the_question = Question.objects.get(pk=question_id) 
                choice = 0
                correctness = 0 
                if question_type == "OE":
                    correctness = 0
                elif question_type == "QA":
                    correctness = 1 if compareTwoStrings(the_question.answer, answer_text) else 2
                elif question_type == "MC":
                    choice = int(answer_text[-1])
                    if the_question.correctOptionEnabled:
                        correctness = 1 if choice == the_question.correctOption else 2
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
        except Question.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Question does not exist.'}) 
    the_project.num_respondents += 1
    the_project.save()  
    return JsonResponse({'status': 'success'})
        

def check_poll_password(request):
    """
    Checks poll password (method = POST)

    ---
    Request requires project id and password
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        project_id_raw = data.get('project')
        project_password = data.get('password')
        if not project_id_raw:
            return JsonResponse({'status': 'error', 'message': 'Invalid Id'})
        
        project_id = int(project_id_raw)
        the_project = Project.objects.get(pk=project_id)

        if the_project.pw == project_password:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Wrong password'})
