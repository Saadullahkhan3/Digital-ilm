from django.shortcuts import render, redirect, get_object_or_404
from .models import QuestionSheet, Question, Student
# Create your views here.
from .forms import TutorRegistrationForm
from django.urls import reverse
from django.contrib.auth import login
from django.http import JsonResponse



def home2(request):
    questions_sheet = QuestionSheet.objects.all()
    return render(request, 'home2.html', {"questions": questions_sheet})

def RegisterTutor(request):
    if request.method == "POST":
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.set_password(form.cleaned_data["password1"])
            tutor.save()
            login(request, tutor)
            return redirect('home2')
    else:
        form = TutorRegistrationForm()
    return render(request, 'registration/login.html', {"form": form})
    



def check_answers(request, db_answers, sheet):
    username = request.POST.get("username")
    score = 0
    print("----------------------------------")
    print(db_answers)
    print("----------------------------------")
    for q_no in db_answers:
        print(q_no)
        if db_answers[q_no] == request.POST.get(q_no):
            print("SCORE UP")
            score += 1
    
    s = Student(name=username, score=score, attempted_sheet=sheet)
    s.save()
    return s

def extract_question_with_id(sheet):
    raw_questions = sheet.all_questions() 
    q = [q.answer_with_id() for q in raw_questions]

    all_answer = {key: value for d in q for key, value in d.items()}

    return all_answer


def get_question_sheet_by_id(request, question_sheet_id):
    # question_sheet = QuestionSheet.objects.get()
    question_sheet = get_object_or_404(QuestionSheet, id=question_sheet_id)
    # return JsonResponse({"msg": "NO"})
    if request.method == "POST":
        answers = extract_question_with_id(question_sheet)
        checked = check_answers(request, answers, question_sheet)

        return render(request, 'leaderboard.html', {"student": checked})
    else:
        raw_questions = question_sheet.all_questions() 

        questions = [q.all() for q in raw_questions]

        
    return render(request, 'question_sheet.html', {"questions": questions, "sheet": question_sheet})



def check_sheet(request, question_sheet_id):
    sheet = QuestionSheet.objects.get(id=question_sheet_id)
    if request.method == "POST": 
            db_answers = extract_question_with_id(sheet)

            username = request.POST.get("username")

            score = 0
            for q_no in db_answers:
                if db_answers[q_no] == request.POST.get(q_no):
                    score += 1


            student = Student(name=username, score=score, questions_sheet=sheet)
            # student.save()

            # data = {"score": score, "user_id": user_id, "username": username, "template_id": template_id}
            return render(request, "check.html", {"student": student})
            
    else:
        raw_questions = sheet.all_questions() 
        questions = [q.all() for q in raw_questions]
        
        return render(request, 'questions.html', {"questions": questions})


