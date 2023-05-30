from django.shortcuts import render
from dashboard.models import Project, Question, Answer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from dashboard.utils import compareTwoStrings


# Create your views here.

def index(request, prj):
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
    # Check if project is being presented
    # if project is being presented:
    # if the_project.is_live:
    #     # Get questions that belong to the project
    #     the_questions = Question.objects.filter(
    #         project=the_project).order_by("position")
    #     print("project is live!")
    #     # Send project and questions to index
    #     return render(request, "poll/index.html", {
    #         "project": the_project,
    #         "questions": the_questions
    #     })
    # else if project not being presented return error page
    # place error page in the website app


# Create function that saves the answers and sends json to update number of votes
# If presentor is showing the results, show error page if person is still trying to cast a vote.

# get the answer sent by JS function submitPollAnswers and save to db
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




# @csrf_exempt
# def get_answers(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         project_id = int(data.get('project'))
#         print(project_id)
#         answers = data.get('answers')
#         if project_id and answers:
#             the_project = Project.objects.get(pk=project_id)
#             # Iterate over the received answers and create new Answer objects
#             for answer_data in answers:
#                 question_id = int(answer_data.get('question'))
#                 answer_text = answer_data.get('answer')
#                 question_type = answer_data.get('type')

#                 if question_id and answer_text and question_type:
#                     # Get Question
#                     the_question = Question.objects.get(pk=question_id)
#                     choice = 0
#                     if question_type == "OE":
#                         correctness = 0
#                     elif question_type == "QA":
#                         if compareTwoStrings(the_question.answer, answer_text):
#                             correctness = 1
#                         else:
#                             correctness = 2
#                     elif question_type == "MC":
#                         if the_question.correctOptionEnabled:
#                             choice = int(answer_text[-1])
#                             if choice == the_question.correctOption:
#                                 correctness = 1
#                             else:
#                                 correctness = 2
#                     else:
#                         return JsonResponse({'status': 'error', 'message': 'Invalid type'})
#                     # Create a new Answer object
#                     answer = Answer(
#                         project=the_project,
#                         question=the_question,
#                         users_answer=answer_text,
#                         users_choice=choice,
#                         is_correct=correctness
#                     )
#                     answer.save()
#             # Update number of respondents on project
#             the_project.num_respondents = the_project.num_respondents + 1
#             the_project.save()

#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid data'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'})





