from django.shortcuts import render
from .models import QuestionSheet, Question, Student
# Create your views here.

def check_answers(request, db_answers, sheet):
    username = request.POST.get("username")
    score = 0
    for q_no in db_answers:
        if db_answers[q_no] == request.POST.get(q_no):
            score += 1

    return Student(name=username, score=score, questions_sheet=sheet)

def extract_question_with_id(sheet):
        raw_questions = sheet.all_questions() 
        q = [q.answer_with_id() for q in raw_questions]

        all_answer = {key: value for d in q for key, value in d.items()}

        return all_answer


def get_question_sheet_by_id(request, question_sheet_id):
    question_sheet = QuestionSheet.objects.get(question_sheet_id)
    if request.method == "POST":
        check_answers(request, "", question_sheet)
    else:
        raw_questions = question_sheet.all_questions() 
        questions = [q.all() for q in raw_questions]
        
        return render(request, 'question_sheet.html', {"questions": questions, "question_sheet_id": question_sheet_id})



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


