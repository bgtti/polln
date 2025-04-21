"""
Dashboard: views pertaining to user (who sets up the polls)
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import Counter
import json
from website.models import User
from dashboard.models import Project, Question, Respondent, Answer, Result
from dashboard.utils import create_prj_code, qr_code_generator, delete_qr_code 

# index is the user's dashboard
@login_required
def index(request, message=None):
    """
    Returns user's dashboard (method = GET)
    """
    user = User.objects.get(pk=request.user.pk)
    projects = Project.objects.filter(user=user).order_by("pk").reverse()
    if not projects:
        projects = None
    # Get message from session storage, and remove it from there
    message = request.session.get('index_message')
    request.session['index_message'] = None
    return render(request, "dashboard/index.html", {
        "projects": projects,
        "message": message
    })


# add new project
def add_project(request):
    """
    Adds a project (method = POST)
    ------------
    Request:
    - project name (projectname string)
    - require username (boolean derived from usernamenabled)
    - require password (string projectpw if pwenabled in request)
    - show answer (string derived from answernabled)
    """
    if request.method == "POST":
        pjt_name = request.POST.get('projectname')
        if not pjt_name:
            request.session['index_message'] = "No project name provided: project could not be saved."
            return HttpResponseRedirect(reverse("dashboard:index"))
        
        user = User.objects.get(pk=request.user.pk)

        if 'usernamenabled' in request.POST:
            set_username = True
        else:
            set_username = False

        if 'pwenabled' in request.POST:
            set_pw = True
            pw = request.POST.get('projectpw', "")
            if not pw or pw == "":
                request.session['index_message'] = "No password set: project could not be saved."
                return HttpResponseRedirect(reverse("dashboard:index"))
        else:
            set_pw = False
            pw=""
        
        if 'answernabled' in request.POST:
            show_answers = True
        else:
            show_answers = False

        try:
            # Save project 
            new_pjt = Project(user=user, name=pjt_name, username_requirement=set_username, pw_requirement=set_pw, pw=pw, show_answers=show_answers)
            new_pjt.save()
            # Give project a prj_code
            prj_code = create_prj_code(request.user.pk, new_pjt.pk)
            new_pjt.prj_code = prj_code
            new_pjt.save()
            # Generate qr code for poll url
            qr_code_generator(prj_code)
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': new_pjt.pk}))
        except:
            print("An error occurred when saving the project")
            request.session['index_message'] = "There was an error saving your project, please try again."
            return HttpResponseRedirect(reverse("dashboard:index"))

# view project page
def project(request, id):
    """
    Shows projects in project template (method = GET)
    """
    try:
        the_project = Project.objects.get(pk=id)
        if the_project.num_questions > 0:
            the_questions = Question.objects.filter(
                project=the_project).order_by("position")
        else:
            the_questions = None
        # Get message from session storage, and remove it from there
        message = request.session.get('project_message')
        request.session['project_message'] = None

        return render(request, "dashboard/project.html", {
            "project": the_project,
            "questions": the_questions,
            "message": message
        })
    except:
        request.session['index_message'] = "There was an error opening your project, please try again."
        return HttpResponseRedirect(reverse("dashboard:index"))        

# Open poll on project
@csrf_exempt
def open_poll(request,id):
    """
    Opens poll (method = GET)

    ---
    Requires project id
    """
    try:
        project = Project.objects.get(pk=id)
        project.is_live = True
        project.save()
        response_data = {'status': 'success', 'message': 'Project is live.'}
        return JsonResponse(response_data)
    except:
        response_data = {'status': 'failure', 'message': 'Could not update project status (open_poll).'}
        return JsonResponse(response_data, status=400)
    
# Close poll on project
@csrf_exempt
def close_poll(request, id):
    """
    Closes poll (method = GET)
    
    ---
    Requires project id
    """
    try:
        project = Project.objects.get(pk=id)
        if project.is_live == True:
            project.is_live = False
            # Check if there are results for the current poll_nr (batch):
            result = Result.objects.filter(project=project, poll_batch=project.poll_nr)
            if not result.exists():
                # If no result matches the poll_nr, check if there are answers to be submitted in this batch. If so, save poll results:
                answers = Answer.objects.filter(project=project, poll_batch=project.poll_nr)
                if answers.exists():
                    questions = Question.objects.filter(project=project)
                    questions_and_correct_answer_total = []
                    for question in questions:
                        sum_correct = 0
                        total_ans = 0
                        all_user_choices = []
                        the_answers = answers.filter(question=question)
                        for answer in the_answers:
                            total_ans += 1
                            if answer.is_correct == 1:
                                sum_correct += 1
                            all_user_choices.append(answer.users_choice)
                        percentage_correct = 0
                        if question.question_type == "Open-ended Question":
                            sum_correct = "N/A"
                        elif question.question_type == "Multiple Choice" and question.correctOption == 0:
                            sum_correct = "N/A"
                        else:
                            percentage_correct = (sum_correct/total_ans)*100
                            if isinstance(percentage_correct, float):
                                percentage_correct = round(percentage_correct, 1)
                            percentage_correct = f"{percentage_correct}%"
                        # convert the list of users choices into a list with the sum of that elements occurence
                        # like: [sum_votes_on_option1, sum_votes_on_option2,....5], when no votes on one of the options, 0
                        # using counter from the collections library: https://docs.python.org/3/library/collections.html#counter-objects
                        choice_results = Counter(all_user_choices)
                        choice_results = [choice_results.get(i, 0) for i in range(1, 6)] 
                        
                        element = {"question_pk": question.pk,
                                    "question": question.question,
                                    "question_type": question.question_type,
                                    "question_num_choices": question.nr_choices,
                                    "question_options": [question.option1, question.option2, question.option3, question.option4, question.option5],
                                    "question_options_chosen_total": choice_results,
                                    "total_answers": total_ans,
                                    "question_has_answer": question.correctOptionEnabled,
                                    "total_correct_ans": sum_correct,
                                    "percentage_ans_that_are_correct": percentage_correct,
                                    }
                        questions_and_correct_answer_total.append(element)

                    json_string = json.dumps(questions_and_correct_answer_total)
                    # create Result object:
                    new_result = Result(
                        project=project, num_respondents=project.num_respondents, question_list_object=json_string)
                    new_result.save()
                    # update Project:
                    project.num_respondents=0
                    project.poll_nr = project.poll_nr + 1

            project.save()
        response_data = {'status': 'success', 'message': 'Project is closed.'}
        return JsonResponse(response_data)
    except:
        response_data = {'status': 'failure',
                        'message': 'Could not update project status (close_poll).'}
        return JsonResponse(response_data, status=400)

# Function that send project data to JS editProjectData function for modal_add_project to edit project, and gets back editted data.
@csrf_exempt
def edit_project(request, id):
    """
    Edit project (methods = GET and POST)

    ---
    GET: will send project data to JS editProjectData function for modal_add_project to enable user to edit project
    POST: changes the project object (name, username requirement, password requirement and password, show answer requirement)

    ---
    Sample data being sent from edit_project when request.method == "GET":
    {
        "model": "dashboard.project",
        "pk": 3,
        "fields": {
            "user": 2,
            "name": "My Pjkt",
            "pw_requirement": false,
            "pw": "",
            "num_questions": 0
        }
    }
    """
    if request.method == "GET":
        project = Project.objects.get(pk=id)
        serialized_question = serialize('json', [project])
        return JsonResponse({'project': serialized_question})
    else:
        if request.method == "POST":
            pjt_name = request.POST['projectname']
            # user = User.objects.get(pk=request.user.pk)
            if 'usernamenabled' in request.POST:
                set_username = True
            else:
                set_username = False
            if 'pwenabled' in request.POST:
                set_pw = True
                pw = request.POST.get('projectpw', "")
                if not pw or pw == "":
                    the_project = Project.objects.get(pk=id)
                    request.session['project_message'] = "No password set, project could not be saved."
                    return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
            else:
                set_pw = False
                pw = ""
            if 'answernabled' in request.POST:
                show_answers = True
            else:
                show_answers = False
            try:
                the_project = Project.objects.get(pk=id)
                the_project.name = pjt_name
                the_project.username_requirement = set_username
                the_project.pw_requirement = set_pw
                the_project.pw = pw
                the_project.show_answers = show_answers
                the_project.save()
                request.session['project_message'] = "Project changes saved successfully!"
                return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
            except:
                request.session['index_message'] = "There was an error editing your project."
                return HttpResponseRedirect(reverse("dashboard:index"))

# deleting a project
def delete_project(request, id):
    """
    Deletes project (method = GET)
    
    ---
    Requires project id
    """
    try:
        the_project = Project.objects.get(pk=id)
        delete_qr_code(the_project.prj_code)
        the_project.delete()
        request.session['index_message'] = "Project deleted successfully!"
        return HttpResponseRedirect(reverse("dashboard:index"))
    except:
        request.session['index_message'] = "There was an error deleting your project, please try again."
        return HttpResponseRedirect(reverse("dashboard:index"))

# adding new question
def add_question(request):
    """
    Adds question (method = POST)
    
    ---
    Request should include: project id, question type, and optionally more question info (answer, options,etc)
    """
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
            request.session['project_message'] = "There was a problem adding your question. Select a question type."
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
        if 'theanswer' in request.POST:
            the_answer = request.POST['theanswer']
        else:
            the_answer = ""
        if 'choiceAnswerEnabled' in request.POST:
            correct_option_enabled = True
            the_correct_choice = int(request.POST['rightChoice'])
        else:
            correct_option_enabled = False
            the_correct_choice = 1
        the_1_option = request.POST.get('choice1', "")
        the_2_option = request.POST.get('choice2', "")
        the_3_option = request.POST.get('choice3', "")
        the_4_option = request.POST.get('choice4', "")
        the_5_option = request.POST.get('choice5', "")

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
            request.session['project_message'] = "Question added successfully!"
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
        except:
            request.session['project_message'] = "There was a problem adding your question. Please try again"
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))

# Question ordering
@csrf_exempt
def question_order(request):
    """
    Defines question order (method = POST)
    
    ---
    question_order gets data from JS getOrderOfQuestions() function and saves the new question position
    Sample json data: {'body': [[1, 0], [2, 1], [3, 2], [4, 3]]}
    Each inner array contains: the question's pk and it's new position. Question order might be important for the user.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get('body', [])
        request.session['index_message'] = None

        for question_data in body:
            if len(question_data) == 2:
                question_pk, position = question_data
                try:
                    question = Question.objects.get(pk=question_pk)
                    question.position = position + 1
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

# Function that sends Question object information to JS the function editQuestionData, and received editted project info. 
@csrf_exempt
def edit_question(request, id):
    """
    Edit question (methods = POST or GET)
    
    ---
    GET: sends question information
    POST: received changed question information

    ---
    Sample data being sent from edit_question when request.method == "GET":
    [
        {
            "model": "dashboard.question",
            "pk": 1,
            "fields": {
                "user": 2,
                "project": 4,
                "question": "How are you today",
                "question_type": "Open-ended Question",
                "answer": null,
                "nr_choices": 0,
                "option1": null,
                "option2": null,
                "option3": null,
                "option4": null,
                "option5": null,
                "correctOptionEnabled": false,
                "correctOption": 1,
                "position": 0
            }
        }
    ]
    """
    if request.method == "GET":
        question = Question.objects.get(pk=id)
        serialized_question = serialize('json', [question])
        return JsonResponse({'question': serialized_question})

    else:
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
            the_project = Project.objects.get(
                pk=int(request.POST['project_pk']))
            request.session['project_message'] = "There was a problem editing your question. Select a question type."
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
        if 'theanswer' in request.POST:
            the_answer = request.POST['theanswer']
        else:
            the_answer = ""
        if 'choiceAnswerEnabled' in request.POST:
            correct_option_enabled = True
            the_correct_choice = int(request.POST['rightChoice'])
        else:
            correct_option_enabled = False
            the_correct_choice = 1
        the_1_option = request.POST['choice1']
        the_2_option = request.POST['choice2']
        the_3_option = request.POST['choice3']
        the_4_option = request.POST['choice4']
        the_5_option = request.POST['choice5']

        try:
            edit_q = Question.objects.get(pk=id)
            edit_q.question = the_question
            edit_q.question_type = the_question_type
            edit_q.answer = the_answer
            edit_q.nr_choices = the_nr_choices
            edit_q.option1 = the_1_option
            edit_q.option2 = the_2_option
            edit_q.option3 = the_3_option
            edit_q.option4 = the_4_option
            edit_q.option5 = the_5_option
            edit_q.correctOptionEnabled = correct_option_enabled
            edit_q.correctOption = the_correct_choice
            edit_q.save()
            request.session['project_message'] = "Question edited successfully!"
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': edit_q.project.pk}))
        except:
            the_project = Project.objects.get(
                pk=int(request.POST['project_pk']))
            request.session['project_message'] = "There was a problem editing your question. Please try again"
            return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))

@csrf_exempt
def delete_question(request, id):
    """
    Deletes question (method = GET)
    
    ---
    Requires question id
    """
    try:
        delete_q = Question.objects.get(pk=id)
        # Update positions of all elements after the element being deleted
        all_q_positioned_after = Question.objects.filter(
            project=delete_q.project, position__gt=delete_q.position)
        for question in all_q_positioned_after:
            question.position -= 1
            question.save()
        # Update the number of questions the project has
        the_project = Project.objects.get(
            pk=delete_q.project.pk)
        the_project.num_questions -= 1
        the_project.save()
        delete_q.delete()
        request.session['project_message'] = "Question deleted successfully!"
        return HttpResponseRedirect(reverse("dashboard:project", kwargs={'id': the_project.pk}))
    except:
        request.session['index_message'] = "There was a problem deleting your question. Please try again"
        return HttpResponseRedirect(reverse("dashboard:index"))


# Project Answers
def project_answers(request, id):
    """
    Gets project answers (method = GET)
    
    ---
    Requires project's id
    """
    the_project = Project.objects.get(pk=id)
    latest_result = Result.objects.filter(project=the_project).order_by('-poll_batch').first()
    latest_respondents = Respondent.objects.filter(
        linked_answer__poll_batch=latest_result.poll_batch, linked_answer__project=the_project).distinct()
    # get object from question_list_object in Result
    json_string = latest_result.question_list_object
    question_results = json.loads(json_string)
    for question in question_results:
        question['question_option_and_total'] = [
            [question['question_options'][i], question['question_options_chosen_total'][i]] for i in range(len(question['question_options']))
        ]
    # get questions
    return render(request, "dashboard/project_answers.html", {
        "project": the_project,
        "results": latest_result,
        "question_results": question_results,
        "respondents": latest_respondents,
    })

# @csrf_exempt 
def set_session_message(request):
    """
    Sets a session message (error/success) (method = POST)
    
    ---
    Requires a string with the message to be displayed
    """
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            request.session["index_message"] = message
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
