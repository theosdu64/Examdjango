from .models import Service
from django import forms

class ServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = ['title', 'description','skill', 'date']
        label = {
            'title': 'Titre',
            'description': 'Description',
            'skill': 'Compétence',
            'date': 'Date',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }