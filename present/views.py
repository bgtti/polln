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


# {
#     "project": "[{\"model\": \"dashboard.project\", \"pk\": 14, \"fields\": {\"user\": 2, \"name\": \"Ma project\", \"username_requirement\": false, \"pw_requirement\": false, \"pw\": \"\", \"show_answers\": true, \"prj_code\": \"002014\", \"is_live\": false, \"poll_nr\": 1, \"num_respondents\": 12, \"num_questions\": 3}}]",
#     "answers": "[{\"model\": \"dashboard.answer\", \"pk\": 1, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-29T11:14:58.366Z\", \"users_answer\": \"good\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 2, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-29T11:17:01.335Z\", \"users_answer\": \"s\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 3, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-29T11:17:01.354Z\", \"users_answer\": \"s\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 4, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-29T11:17:01.372Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 5, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-29T11:19:38.276Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 6, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-29T11:19:38.294Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 7, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-29T11:19:38.311Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 8, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-29T11:19:56.563Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 9, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-29T11:19:56.582Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 10, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-29T11:19:56.598Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 11, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-29T11:21:27.630Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 12, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-29T11:21:27.650Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 13, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-29T11:21:27.669Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 14, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T12:53:31.682Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 15, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T12:53:31.692Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 16, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T12:53:31.710Z\", \"users_answer\": \"ff\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 17, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T13:08:21.168Z\", \"users_answer\": \"ddd\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 18, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T13:08:21.188Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 19, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T13:08:21.211Z\", \"users_answer\": \"fff\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 20, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T13:10:20.396Z\", \"users_answer\": \"fff\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 21, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T13:10:20.404Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 22, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T13:10:20.438Z\", \"users_answer\": \"dd\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 23, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T13:12:56.866Z\", \"users_answer\": \"j\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 24, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T13:12:56.886Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 25, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T13:12:56.902Z\", \"users_answer\": \"g\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 26, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T14:28:26.044Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 27, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T14:28:26.069Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 28, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T14:28:26.088Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 29, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T20:28:04.685Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 30, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T20:28:04.700Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 31, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T20:28:04.716Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 32, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 15, \"submission_date\": \"2023-05-30T20:28:33.697Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 0}}, {\"model\": \"dashboard.answer\", \"pk\": 33, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 17, \"submission_date\": \"2023-05-30T20:28:33.705Z\", \"users_answer\": \"option2\", \"users_choice\": 2, \"is_correct\": 2}}, {\"model\": \"dashboard.answer\", \"pk\": 34, \"fields\": {\"project\": 14, \"poll_batch\": 1, \"question\": 16, \"submission_date\": \"2023-05-30T20:28:33.734Z\", \"users_answer\": \"d\", \"users_choice\": 0, \"is_correct\": 2}}]"
# }
