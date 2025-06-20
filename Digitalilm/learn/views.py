from .models import QuestionSheet, Question, Student
from .forms import TutorRegistrationForm, QuestionSheetForm, QuestionForm, QuestionModelFormSet

from django.forms import modelformset_factory, formset_factory

from django.db.models import Q

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from pprint import pprint



# ---------------- General -----------------
def explore_quizzes(request):
    valid_levels = QuestionSheet.get_levels()
    tutors = User.objects.all()
    levels = request.GET.get('level', '').split(',')
    tutor = request.GET.get('tutor')
    title = request.GET.get('title')

    filters = Q()
    if levels and levels != ['']:
        levels = [int(level) for level in levels if level.isdigit() and int(level) in valid_levels]
        if levels:
            filters &= Q(level__in=levels)

    if tutor:
        filters &= Q(tutor__username__icontains=tutor)
        
    if title:
        filters &= Q(title__icontains=title)

    if filters:
        question_sheets = QuestionSheet.objects.filter(filters)
    else:
        question_sheets = QuestionSheet.objects.all()
    
    return render(request, 'explore_quizzes.html', {
        "question_sheets": question_sheets,
        "valid_levels": valid_levels,
        "tutors": tutors
    })



# ---------------- Student -----------------
# [INTERNAL USAGE]
def check_answers(request, db_answers, sheet):
    username = request.POST.get("username")
    score = 0

    for q_no in db_answers:
        if db_answers[q_no] == request.POST.get(q_no):
            score += 1
    
    s = Student(name=username, score=score, attempted_sheet=sheet)
    s.save()
    return s


# [INTERNAL USAGE]
def extract_question_with_id(sheet):
    raw_questions = sheet.questions.all()
    q = [q.answer_with_id() for q in raw_questions]

    all_answer = {key: value for d in q for key, value in d.items()}

    return all_answer


def question_sheet_by_id(request, question_sheet_id):
    # Use filter to prevernt not found error error!
    raw_question_sheet = QuestionSheet.objects.filter(id=question_sheet_id)

    if not raw_question_sheet:
        return render(request, 'question_sheet.html', {"found": 0})

    # Re-assign to use it as normal when we confirm that this sheet is exists!
    question_sheet = raw_question_sheet[0]

    if request.method == "POST":
        answers = extract_question_with_id(question_sheet)
        student = check_answers(request, answers, question_sheet)

        return redirect(reverse('leaderboard_by_id', kwargs={'question_sheet_id': question_sheet_id}) + f'?redirected=true&student_id={student.id}')

        # return redirect('leaderboard_by_id', question_sheet_id, kwargs={"student":student})
    
    else:
        raw_questions = question_sheet.questions.all()

        questions = [q.all() for q in raw_questions]

    return render(request, 'question_sheet.html', {"question_sheet": question_sheet, "questions": questions})


def leaderboard_by_id(request, question_sheet_id):
    # Use filter to prevernt not found error error!
    raw_question_sheet = QuestionSheet.objects.filter(id=question_sheet_id)

    if not raw_question_sheet:
        return render(request, 'question_sheet.html', {"found": 0})

    # Re-assign to use it as normal when we confirm that this sheet is exists!
    question_sheet = raw_question_sheet[0]

    all_students = Student.objects.filter(attempted_sheet=question_sheet.id)

    # Check if this request is a redirection after submission
    redirected = request.GET.get('redirected', False)
    
    _student_id: str = request.GET.get('student_id', "") 
    student_id = int(_student_id) if _student_id.isdigit() else None 

    student = None
    # If redirected, fetch the student information
    if redirected and student_id:
        # Check that provided id of student exists and also related to provided sheet to prevent irrelevant relationship
        _student = Student.objects.filter(id=student_id, attempted_sheet=question_sheet.id)
        student = _student[0] if _student else None

    return render(request, 'leaderboard.html', {"question_sheet": question_sheet, "student": student, "all_students": all_students, "redirected": redirected})
    


# ---------------- Tutor -----------------
def tutor_register(request):
    if request.method == "POST":
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            tutor = form.save(commit=False)
            tutor.set_password(form.cleaned_data["password1"])
            tutor.save()
            login(request, tutor)
            return redirect('home')
    else:
        form = TutorRegistrationForm()
    return render(request, 'registration/register.html', {"form": form})


@login_required
def tutor_profile(request):
    # tutor = get_object_or_404(User, id=request.user.id)
    tutor = User.objects.get(id=request.user.id)

    questions_sheet = QuestionSheet.objects.filter(tutor=tutor.id)

    if not questions_sheet.exists():
        # Handle the case where no sheets are found
        pass

    return render(request, 'tutor.html', {"tutor": tutor, "questions_sheet": questions_sheet})


@login_required
def confirm_logout(request):
    return render(request, 'registration/logout.html')



# ---------------- Question Sheet ------------------
# [INTERNAL USAGE]
@login_required
def _get_question_form(request):
    index = request.GET.get('index', 0)
    QuestionFormSet = formset_factory(QuestionForm, extra=1)  # Create formset dynamically
    form = QuestionFormSet().forms[0]  # Only get the first form

    return JsonResponse({
        'html': form.as_p().replace('id_form-0-', f'id_form-{index}-').replace('form-0-', f'form-{index}-')
    })


@login_required
def create_question_sheet(request):
    # Dynamically handle multiple questions
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, formset=QuestionModelFormSet, fields=('question', 'answer', 'a', 'b', 'c', 'd'), extra=1)

    if request.method == 'POST':
        question_sheet_form = QuestionSheetForm(request.POST)
        formset = QuestionFormSet(request.POST, queryset=Question.objects.none())

        if question_sheet_form.is_valid() and formset.is_valid():
            # Save QuestionSheet instance(Not in Database)
            question_sheet = question_sheet_form.save(commit=False)
            question_sheet.tutor = request.user 
            question_sheet.save()

            for form in formset:
                # Skipping blank forms
                if not form.cleaned_data:
                    continue

                question = form.save(commit=False)
                question.question_sheet = question_sheet
                question.save()
                    
            formset.save()

            return redirect('question_sheet_by_id', question_sheet.id)
    else:
        question_sheet_form = QuestionSheetForm()
        formset = QuestionFormSet(queryset=Question.objects.none())

    return render(request, 'create_question_sheet.html', {
        'question_sheet_form': question_sheet_form,
        'formset': formset,
    })


@login_required
def edit_sheet(request, question_sheet_id):
    # Dynamically handle multiple questions
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, formset=QuestionModelFormSet, fields=('question', 'answer', 'a', 'b', 'c', 'd'), extra=0, can_delete=True)

    _question_sheet = QuestionSheet.objects.filter(id=question_sheet_id, tutor=request.user)

    if not _question_sheet:
        return render(request, 'edit_sheet.html', {"found": 0})

    # Accessing question sheet object when it found
    _question_sheet = _question_sheet[0]

    _questions = Question.objects.filter(question_sheet=_question_sheet.id)
    
    if request.method == 'POST':
        question_sheet_form = QuestionSheetForm(request.POST, instance=_question_sheet)
        formset = QuestionFormSet(request.POST, queryset=_questions)

        if question_sheet_form.is_valid() and formset.is_valid():
            question_sheet = question_sheet_form.save(commit=False)
            question_sheet.save()
            
            for form in formset:
                # Skipping blank forms
                if not form.cleaned_data:
                    continue

                if form.cleaned_data.get('DELETE'):
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    question = form.save(commit=False)
                    question.question_sheet = question_sheet
                    question.save()
                    
            formset.save()

            return redirect('question_sheet_by_id', question_sheet.id)
    else:
        question_sheet_form = QuestionSheetForm(instance=_question_sheet)
        formset = QuestionFormSet(queryset=_questions)

    return render(request, 'edit_sheet.html', {
        'question_sheet_form': question_sheet_form,
        'formset': formset,
    })


@login_required
def delete_sheet(request, question_sheet_id):
    found = 1
    sheet = QuestionSheet.objects.filter(id=question_sheet_id, tutor=request.user)
    if sheet:
        if request.method == "POST":
            sheet.delete()  
            return redirect("tutor")
    else:
        found = 0

    return render(request, 'confirm_sheet_delete.html', {"question_sheet_id": question_sheet_id, "found": found})

    
    

