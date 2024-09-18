from .models import QuestionSheet, Question, Student
from .forms import TutorRegistrationForm, QuestionSheetForm, QuestionForm

from django.forms import modelformset_factory

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User 


def modify_nav(request):
    ok = 0
    tutor_username = None 
    if request.user.is_authenticated:
        ok = 1
        tutor_username = request.user.username
    
    return ok, tutor_username



def get_question_form(request):
    index = int(request.GET.get('index'))
    
    form = QuestionForm(prefix=index)
    data = {
        'html': render_to_string('question_form.html', {'form': form}),
        'order': index + 1,  # Return the order of the question
        'id': f"question-{index}"  # Return a unique id for the question
    }
    
    return JsonResponse(data)

@login_required
def after_tutor_register(request):
    ok, tutor_username = modify_nav(request)



    tutor = get_object_or_404(User, id=request.user.id)

    sheets = QuestionSheet.objects.filter(tutor=tutor.id)
    if not sheets.exists():
        # Handle the case where no sheets are found
        pass


    return render(request, 'tutor.html', {"tutor": tutor, "questions": sheets, "tutor_username": tutor_username, "ok": ok})



@login_required
def create_question_sheet2(request):
    ok, tutor_username = modify_nav(request)

    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)  # Dynamically handle multiple questions

    if request.method == 'POST':
        question_sheet_form = QuestionSheetForm(request.POST)
        formset = QuestionFormSet(request.POST, queryset=Question.objects.none())

        if question_sheet_form.is_valid() and formset.is_valid():
            # Save QuestionSheet
            question_sheet = question_sheet_form.save(commit=False)
            question_sheet.tutor = request.user  # Assuming user is logged in as tutor
            question_sheet.save()

            # Save each question and link it to the question sheet
            for form in formset:
                question = form.save(commit=False)
                question.question_sheet = question_sheet
                question.save()
            return redirect('question_sheet_id', question_sheet.id)
    else:
        question_sheet_form = QuestionSheetForm()
        formset = QuestionFormSet(queryset=Question.objects.none())  # Empty formset

    return render(request, 'create_question_sheet.html', {
        'question_sheet_form': question_sheet_form,
        'formset': formset,

        "tutor_username": tutor_username, "ok": ok
    })





def home2(request):
    ok, tutor_username = modify_nav(request)
    questions_sheet = QuestionSheet.objects.all()
    return render(request, 'home2.html', {"questions": questions_sheet, "tutor_username": tutor_username, "ok": ok})


def RegisterTutor(request):
    ok, tutor_username = modify_nav(request)


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
    return render(request, 'registration/login.html', {"form": form, "tutor_username": tutor_username, "ok": ok})


def check_answers(request, db_answers, sheet):
    username = request.POST.get("username")
    score = 0

    for q_no in db_answers:
        if db_answers[q_no] == request.POST.get(q_no):
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
    ok, tutor_username = modify_nav(request)

    question_sheet = get_object_or_404(QuestionSheet, id=question_sheet_id)

    if request.method == "POST":
        answers = extract_question_with_id(question_sheet)
        checked = check_answers(request, answers, question_sheet)

        return render(request, 'leaderboard.html', {"student": checked})
    else:
        raw_questions = question_sheet.all_questions() 

        questions = [q.all() for q in raw_questions]

        
    return render(request, 'question_sheet.html', {"questions": questions, "sheet": question_sheet, "tutor_username": tutor_username, "ok": ok})


def check_sheet(request, question_sheet_id):
    ok, tutor_username = modify_nav(request)

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
            return render(request, "check.html", {"student": student, "tutor_username": tutor_username, "ok": ok})
            
    else:
        raw_questions = sheet.all_questions() 
        questions = [q.all() for q in raw_questions]
        
        return render(request, 'questions.html', {"questions": questions})


