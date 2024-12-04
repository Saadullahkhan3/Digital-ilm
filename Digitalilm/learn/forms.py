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
        #         'name': 'form-control'
        #     }),
        #     'answer': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     'a': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     'b': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     'c': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     }),
        #     'd': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     })
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
                'id': 'id_name',
                'placeholder': 'Enter name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_username',
                'placeholder': 'Enter username'
            }),
            'email' : forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'id_email',
                'placeholder': 'Enter your email'
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



# class QuestionSheetForm(forms.ModelForm):
#     class Meta:
#         model = QuestionSheet  
