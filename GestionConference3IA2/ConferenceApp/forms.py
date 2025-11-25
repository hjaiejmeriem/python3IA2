from django import forms
from .models import Conference, Submission

# ============================
# Formulaire de Conference
# ============================
class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        
        # Les champs du formulaire
        fields = ['name', 'theme', 'location', 'description', 'start_date', 'end_date']
        
        # Les labels affichés dans la page HTML
        labels = {
            'name': "Titre de la conférence",
            'theme': "Thématique de la conférence",
        }

        # Personnalisation des widgets
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "Entrer un titre à la conférence"
            }),
            'start_date': forms.DateInput(attrs={
                'type': "date"
            }),
            'end_date': forms.DateInput(attrs={
                'type': "date"
            }),
            # Exemple : rendre la description plus confortable
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Décrivez la conférence..."
            }),
        }


# ============================
# Formulaire de Submission
# ============================
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        
        # Champs à afficher
        fields = ['title', 'abstract', 'keywords', 'paper', 'conference']

        # Widgets recommandés pour un bon rendu
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5}),
            'keywords': forms.TextInput(attrs={'placeholder': "ex: IA, deep learning, data"}),
        }
