from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from .models import QuestionSheet, Question

class InputWrapper(forms.TextInput):
    def __init__(self, add_on=None, *args, **kwargs):
        self.add_on = add_on
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Render the input field
        input_html = super().render(name, value, attrs, renderer)
        # Wrap it in a div with an optional add-on
        if self.add_on:
            return mark_safe(f'<div class="input-group"><label class="input-group-text">{self.add_on}</label>{input_html}</div>')
        return mark_safe(f'<div>{input_html}</div>')  # No add-on

class QuestionSheetForm(forms.ModelForm):
    class Meta:
        model = QuestionSheet
        fields = ['title', 'level']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer', 'a', 'b', 'c', 'd']
        widgets = {
            'question': InputWrapper(add_on='Question'),
            'answer': InputWrapper(add_on='Anwser'),
            'a': InputWrapper(add_on="A"),
            'b': InputWrapper(add_on="B"),
            'c': InputWrapper(add_on="C"),
            'd': InputWrapper(add_on="D"),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize labels to use <span> instead of default labels
        for field in self.fields:
            print(self.fields[field].label)
            # self.fields[field].label = f'<span>{self.fields[field].label}</span>'
            self.fields[field].label = mark_safe('')

        # Set the class for all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


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
