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