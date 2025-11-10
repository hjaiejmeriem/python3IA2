from django import forms
from .models import Conference, Submission

class ConferenceForm(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','location','description','start_date','end_date']
        labels = {
            'name':"titre de la conférence",
            'theme':"Thématique de la conférence",
        }
        widgets ={
            'name' : forms.TextInput(
                attrs= {
                    'placeholder' :"Entrer un titre à la conférence" 
                }
            ),
            'start_date' : forms.DateInput(
                attrs ={
                    'type':"date"
                }
            ),
            'end_date' : forms.DateInput(
                attrs ={
                    'type':"date"
                }
            )
        }
#to add for homework 10
# Formulaire pour Conference
class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['name', 'theme', 'location', 'description', 'start_date', 'end_date']
        labels = {
            'name': "Titre de la conférence",
            'theme': "Thématique de la conférence",
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Entrer un titre à la conférence"}),
            'start_date': forms.DateInput(attrs={'type': "date"}),
            'end_date': forms.DateInput(attrs={'type': "date"}),
        }

# Formulaire pour Submission
# forms.py
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference']