from django import forms
from .models import Conference

class ConferenceForm(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name' , 'theme' , 'location' , 'description' , 'start_date' , 'end_date']
        labels={
            'name':"Titre de la conférence",
            'theme':"Thème de la conférence",
        }
        widgets={
            'name': forms.TextInput(attrs={'placeholder':"Entrer le titre de la conférence"}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }