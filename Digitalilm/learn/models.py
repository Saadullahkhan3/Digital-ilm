from django.db import models
from django.contrib.auth.models import User 



# on_delete=models.CASCADE
'''
It deletes related things, such as
When a User(Tutor) deletes its account then question sheets which are related to this Tutor will also be deleted and because question sheets are deleted then questions which are related to question sheet will also be deleted
BUT it not happened in reverse order, means if any question is deleted, it not auto delete related question sheet and also when any question sheet deleted, it not also delete Tutor account.
It works like a tree, where if root removed entire tree falldown but if any leaf dead, nothing happened to root.
               User
                |
        -------------------
        |                 |
    QuestionSheet      QuestionSheet  
        |                  |
    -----------        -----------
    |         |        |         |
Question  Question     Question   Question
'''



class QuestionSheet(models.Model):
    title = models.CharField(max_length=200)

    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tutor")
    
    l = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),              
        (5, 5)]
    level = models.IntegerField(choices=l, default=1)

    # description = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # attempted_count = models.IntegerField(default=0)


    def __str__(self):
        return self.title


    @classmethod
    def get_levels(cls):
        return [choice[0] for choice in cls._meta.get_field('level').choices]



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

    question_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE, related_name="questions")


    def __str__(self):
        return self.question


    def answer_with_id(self):
        return {f"{self.id}" : self.answer}


    def all(self):
        def create_options_dict(*options):
            options_dict = dict()
            for key, value in zip(("a", "b", "c", "d"), *options):
                options_dict[key] = value
            return options_dict
        
        options = [option for option in (self.a, self.b, self.c, self.d) if option]

        return {"id": self.id, "question": self.question, "options": create_options_dict(options)}



class Student(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    
    attempted_sheet = models.ForeignKey(QuestionSheet, on_delete=models.CASCADE, related_name="attempted_sheet")


    def __str__(self):
        return f"{self.name, 25} | {self.score}"
    


