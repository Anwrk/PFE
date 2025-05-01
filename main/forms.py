# forms.py
from django import forms
from .models import Register, Question, Form

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name', 'email', 'age','user_id', 'phone_num', 'education_level']


class DynamicForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            field_name = str(question.id)
            if question.type == Question.TEXT:
                self.fields[field_name] = forms.CharField(label=question.text, required=True)
            elif question.type == Question.PARAGRAPH:
                self.fields[field_name] = forms.CharField(label=question.text, required=True, widget=forms.Textarea)
            elif question.type in [Question.CHOICE, Question.DROPDOWN, Question.MULTICHOICE]:
                choices_list = [(c.strip(), c.strip()) for c in question.choices.split(',') if c.strip()]
                if question.type == Question.CHOICE:
                    self.fields[field_name] = forms.ChoiceField(label=question.text, widget=forms.RadioSelect, choices=choices_list)
                elif question.type == Question.DROPDOWN:
                    self.fields[field_name] = forms.ChoiceField(label=question.text, widget=forms.Select, choices=choices_list)
                elif question.type == Question.MULTICHOICE:
                    self.fields[field_name] = forms.MultipleChoiceField(
                        label=question.text,
                        widget=forms.CheckboxSelectMultiple,
                        choices=choices_list
                    )


class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title']

QuestionFormSet = forms.inlineformset_factory(
    Form, Question,
    fields=['text', 'type', 'choices'],
    extra=1,  # عدد الأسئلة الافتراضية
    can_delete=False
)

