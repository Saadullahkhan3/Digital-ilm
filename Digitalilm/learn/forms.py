from .models import QuestionSheet, Question

from django import forms
from django.forms import BaseModelFormSet

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError  # For raising validation errors in the form [just keep it so I knew what I did]


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



class TextareaWrapper(forms.Textarea):
    def __init__(self, add_on=None, *args, **kwargs):
        self.add_on = add_on
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        textarea_html = super().render(name, value, attrs, renderer)
        if self.add_on:
            return mark_safe(f'''<p class="input-group"><label class="input-group-text">{self.add_on}</label>{textarea_html}</p>''')
        return mark_safe(f'<div>{textarea_html}</div>')  
    
    
    
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

    def clean(self):
        cleaned_data = super().clean()
        c = cleaned_data.get("c")
        d = cleaned_data.get("d")
        answer = cleaned_data.get("answer")

        # Check if C is blank but D exists
        if not c and d:
            self.add_error('c', "Option C can't be blank if Option D exists")

        # Check if the chosen answer is blank
        if cleaned_data.get(answer) is None:
            self.add_error('answer', "Chosen answer can't be blank")

        return cleaned_data
         
         
         
class QuestionSheetForm(forms.ModelForm):
    class Meta:
        model = QuestionSheet
        fields = ['title', 'level', 
                #   'description'
                  ]
        widgets = {
            'title': InputWrapper(add_on="Title"),
            'level': InputSelectWrapper(add_on="Level"),
            # 'description': TextareaWrapper(add_on="Description"),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_label(self.fields)
        # add_custom_classes(self.fields.values())
        
                 

class TutorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

