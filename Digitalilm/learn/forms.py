from django import forms
from django.contrib.auth.models import User
from .models import QuestionSheet

class TutorRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")



# class QuestionSheetForm(forms.ModelForm):
#     class Meta:
#         model = QuestionSheet  
