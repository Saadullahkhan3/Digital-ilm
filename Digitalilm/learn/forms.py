from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import QuestionSheet, Question

class QuestionSheetForm(forms.ModelForm):
    class Meta:
        model = QuestionSheet
        fields = ['title', 'level']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer', 'a', 'b', 'c', 'd']
        # widgets = {
        #     'question': forms.TextInput(attrs={
        #         'name': 'form-puppo-1'
        #     }),
        #     'answer': forms.TextInput(attrs={
        #         'name': 'form-puppo-2'
        #     }),
        #     'a': forms.TextInput(attrs={
        #         'name': 'form-puppo-3'
        #     }),
        #     'b': forms.TextInput(attrs={
        #         'name': 'form-puppo-4'
        #     }),
        #     'c': forms.TextInput(attrs={
        #         'name': 'form-puppo-5'
        #     }),
        #     'd': forms.TextInput(attrs={
        #         'name': 'form-puppo-6'
        #     }),
        # }


class TutorRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("name", "username", "email", "password1", "password2")
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Enter name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_username',
                'placeholder': 'Enter username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'id_password1',
                'placeholder': 'Enter password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'id': 'id_password2',
                'placeholder': 'Confirm password'
            }),
        }



# class QuestionSheetForm(forms.ModelForm):
#     class Meta:
#         model = QuestionSheet  
