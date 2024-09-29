from .models import QuestionSheet, Question, Student
from .forms import TutorRegistrationForm, QuestionSheetForm, QuestionForm

from django.forms import modelformset_factory, formset_factory

from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User 

from pprint import pprint

# ---------------- General -----------------
def explore_quizzes(request):
    questions_sheet = QuestionSheet.objects.all()
    return render(request, 'explore_quizzes.html', {"questions": questions_sheet})



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
    raw_questions = sheet.all_questions() 
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

        return redirect(reverse('leaderboard_by_id', kwargs={'question_sheet_id': question_sheet_id}) + f'?redirected=true&student={student.id}')

        # return redirect('leaderboard_by_id', question_sheet_id, kwargs={"student":student})
    
    else:
        raw_questions = question_sheet.all_questions() 

        questions = [q.all() for q in raw_questions]

    return render(request, 'question_sheet.html', {"questions": questions, "sheet": question_sheet})


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
    
    _student_id = request.GET.get('student', None) 
    student_id = int(_student_id) if _student_id.isdigit() else None 

    # If redirected, fetch the student information
    if redirected and student_id:
        student = Student.objects.filter(id=student_id)

    return render(request, 'leaderboard.html', {"student": student, "all_students": all_students, "redirected": redirected})
    


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

    sheets = QuestionSheet.objects.filter(tutor=tutor.id)

    if not sheets.exists():
        # Handle the case where no sheets are found
        pass

    return render(request, 'tutor.html', {"tutor": tutor, "questions": sheets})


@login_required
def confirm_logout(request):
    return render(request, 'registration/logout.html')



# ---------------- Question Sheet ------------------

# [INTERNAL USAGE]
@login_required
def get_question_form(request):
    index = request.GET.get('index', 0)
    QuestionFormSet = formset_factory(QuestionForm, extra=1)  # Create formset dynamically
    form = QuestionFormSet().forms[0]  # Only get the first form

    return JsonResponse({
        'html': form.as_p().replace('id_form-0-', f'id_form-{index}-').replace('form-0-', f'form-{index}-')
    })


@login_required
def create_question_sheet(request):
    # Dynamically handle multiple questions
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)  

    if request.method == 'POST':
        question_sheet_form = QuestionSheetForm(request.POST)
        formset = QuestionFormSet(request.POST, queryset=Question.objects.none())

        if question_sheet_form.is_valid() and formset.is_valid():
            # Save QuestionSheet instance(Not in Database)
            question_sheet = question_sheet_form.save(commit=False)
            question_sheet.tutor = request.user 
            question_sheet.save()

            # Save each question and link it to the question sheet
            for form in formset:
                question = form.save(commit=False)
                question.question_sheet = question_sheet
                question.save()
            # Showing new created Question sheet 
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
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=0, can_delete=True)  

    _question_sheet = QuestionSheet.objects.get(id=question_sheet_id, tutor=request.user)
    _questions = Question.objects.filter(question_sheet=_question_sheet.id)
    if request.method == 'POST':
        # pprint(dict(request.POST), indent=4)

        question_sheet_form = QuestionSheetForm(request.POST, instance=_question_sheet)
        formset = QuestionFormSet(request.POST, queryset=_questions)

        if question_sheet_form.is_valid() and formset.is_valid():
            # Save QuestionSheet instance(Not in Database)
            question_sheet = question_sheet_form.save(commit=False)
            question_sheet.save()
            
            # Save each question and link it to the question sheet
            for form in formset:
                if form.cleaned_data.get('DELETE'):  # Check if the form is marked for deletion
                    if form.instance.pk:  # Check if the question already exists in the database
                        form.instance.delete()  # Delete the question from the database
                else:
                    question = form.save(commit=False)  # Save the question
                    question.question_sheet = question_sheet
                    question.save()

            # Showing new created Question sheet 
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

    
    

    


   


        
'''
redirect war gaya
'''