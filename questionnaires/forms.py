from django import forms
from .models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['title', 'description', 'image', 'final_statement', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Insert questionnaire description', 
                'rows': 4,
                'maxlength': '500'
            }),
            'final_statement': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Insert the final statement', 
                'rows': 3,
                'maxlength': '300'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
