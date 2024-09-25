from .models import QuestionSheet, Question, Student
from .forms import TutorRegistrationForm, QuestionSheetForm, QuestionForm

from django.forms import modelformset_factory

from django.shortcuts import render, redirect
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.models import User 


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
        return render(request, 'question_sheet.html', {"questions_found": 0})

    # Re-assign to use it as normal when we confirm that this sheet is exists!
    question_sheet = raw_question_sheet[0]

    if request.method == "POST":
        answers = extract_question_with_id(question_sheet)
        checked = check_answers(request, answers, question_sheet)

        # Shayan Adnan,
        # Create Leaderboard for specific question sheet that can be pass into redirect() but for this you need to define a url in learn/urls.py and keep that url(added by you) name 'leaderboard'
        return render(request, 'leaderboard.html', {"student": checked})
    
    else:
        raw_questions = question_sheet.all_questions() 

        questions = [q.all() for q in raw_questions]

    return render(request, 'question_sheet.html', {"questions": questions, "sheet": question_sheet})



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
    index = int(request.GET.get('index'))
    
    form = QuestionForm(prefix=index)
    data = {
        'html': render_to_string('question_form.html', {'form': form}),
        'order': index + 1,  # Return the order of the question
        'id': f"question-{index}"  # Return a unique id for the question
    }
    
    return JsonResponse(data)


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


# Shayan Adnan,
# Create edit functionality for Question Sheet but keep in mind that we not used normal form we use form-factory which needed to be learn
# this edit functionality should be available in tutor.html, change Edit button href attribute that looks like:
# href="{% url 'question_sheet_by_id' question.id %}"
# Get absolute hints by create_question_sheet() function that how it works!
@login_required
def edit_sheet(request):
    if request.method == "POST":
        pass
    else:
        form = None 
    return render(request, '')











   


        




# def LoginTutor(request):
#     if request.method == "POST":
#         form = TutorRegistrationForm(request.POST)
#         if form.is_valid():
#             login(request, form)
#     else:
#         form = TutorRegistrationForm()
#     return render(request, 'registration/login.html', {"form": form})