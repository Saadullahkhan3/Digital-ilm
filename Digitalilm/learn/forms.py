from .models import QuestionSheet, Question

from django import forms
from django.forms import BaseModelFormSet

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.utils.safestring import mark_safe


class QuestionModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def total_form_count(self):
        # Use the largest index from the POST data instead of consecutive counting
        if self.data:
            max_index = 0
            for key in self.data.keys():
                # Look for form-TXYZ-question pattern or similar
                if key.startswith(f'{self.prefix}-') and key.endswith('-question'):
                    # Extract form index
                    parts = key.split('-')
                    try:
                        idx = int(parts[1])
                        if idx > max_index:
                            max_index = idx
                    except ValueError:
                        pass
            # Add 1 because indices are zero-based
            return max_index + 1
        return super().total_form_count()

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        
        print(f"WOW -> {self.forms}")
        
        # Remove or comment out any 'order' reindexing
        for i, form in enumerate(self.forms):
            if self.can_delete and self._should_delete_form(form):
                continue


def remove_label(self_fields):
    for field in self_fields:
        self_fields[field].label = mark_safe('')


def add_custom_classes(self_fields_values):
    for field in self_fields_values:
        if isinstance(field, forms.TypedChoiceField):
            field.widget.attrs['class'] = 'form-select'
            continue
            
        field.widget.attrs['class'] = 'form-control'



class InputWrapper(forms.TextInput):
    def __init__(self, add_on=None, another_add_on=None,  *args, **kwargs):
        self.add_on = add_on
        self.another_add_on = another_add_on      
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, renderer=None):
        # Render the input field
        input_html = super().render(name, value, attrs, renderer)
        # Wrap it in a div with an optional add-on
        if self.add_on:
            return mark_safe(f'''<p class="input-group"><label class="input-group-text">{self.add_on}</label>{input_html}{f'<span class="input-group-text">{self.another_add_on}</span>' if self.another_add_on else ""}</p>''')
        return mark_safe(f'<div>{input_html}</div>')  # No add-on



class InputSelectWrapper(forms.Select):
    def __init__(self, add_on=None, another_add_on=None, *args, **kwargs):
        self.add_on = add_on
        self.another_add_on = another_add_on
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, renderer=None):
        # Render the input field
        input_html = super().render(name, value, attrs, renderer)
        # Wrap it in a div with an optional add-on
        if self.add_on:
            return mark_safe(f'''<p class="input-group w-fit-content"><label class="input-group-text">{self.add_on}</label>{input_html}{f'<span class="input-group-text">{self.another_add_on}</span>' if self.another_add_on else ""}</p>''')
        return mark_safe(f'<div>{input_html}</div>')  # No add-on



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer', 'a', 'b', 'c', 'd']
        widgets = {
            'question': InputWrapper(add_on='Question'),
            'answer': InputSelectWrapper(add_on='Answer'),
            'a': InputWrapper(add_on="A"),
            'b': InputWrapper(add_on="B"),
            'c': InputWrapper(add_on="C", another_add_on="Optional"),
            'd': InputWrapper(add_on="D", another_add_on="Optional"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_label(self.fields)
        add_custom_classes(self.fields.values())
         
         
         
class QuestionSheetForm(forms.ModelForm):
    class Meta:
        model = QuestionSheet
        fields = ['title', 'level']
        widgets = {
            'title': InputWrapper(add_on="Title"),
            'level': InputSelectWrapper(add_on="Level")
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_label(self.fields)
        # add_custom_classes(self.fields.values())
        
                 

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
