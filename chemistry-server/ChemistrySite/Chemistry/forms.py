# forms.py
from django import forms
from .models import Decision


class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ['answer']
        widgets = {
            'answer': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)  # Извлекаем вопрос из параметров
        super().__init__(*args, **kwargs)
        # Фильтруем ответы для конкретного вопроса
        if question:
            self.fields['answer'].queryset = question.answers_set.all()
