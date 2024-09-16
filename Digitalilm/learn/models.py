from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class QuestionSheet(models.Model):
    title = models.CharField(max_length=200)

    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tutor")


    def all_questions(self):
        return self.question_sheet.all()



class Question(models.Model):

    OPTIONS = [
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
        ("d", "d"),
    ]

    question = models.CharField(max_length=500)

    answer = models.CharField(max_length=1, choices=OPTIONS)

    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100, blank=True, null=True)
    d = models.CharField(max_length=100, blank=True, null=True)

    question_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE, related_name="question_sheet")


    def all(self):
        def create_options_dict(*options):
            options_dict = dict()
            for key, value in zip(("a", "b", "c", "d"), *options):
                options_dict[key] = value
            return options_dict
        
        options = [option for option in (self.a, self.b, self.c, self.d) if option]

        return {"question": self.q, "options": create_options_dict(options)}



class Student(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()

    attempted_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE, related_name="questions_sheet")


    def __str__(self):
        def truncate(string, max_length):
            if len(string) > max_length:
                return string[:max_length]
            return string

        return f"{truncate(self.name, 25)} | {self.score}"
    


