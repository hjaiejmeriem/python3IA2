from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """
    Formulaire personnalisé pour l'inscription d'un nouvel utilisateur.
    Hérite de UserCreationForm pour gérer automatiquement :
    - la validation des mots de passe
    - la sécurité
    - la confirmation password1/password2
    """

    class Meta:
        model = User  # Utilise ton modèle User personnalisé
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'affiliation', 'nationality',
            'password1', 'password2'
        ]

        # Permet de personnaliser l'apparence des champs
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': "Email universitaire",
                'class': "form-control"
            }),

            'password1': forms.PasswordInput(attrs={
                'class': "form-control"
            }),

            'password2': forms.PasswordInput(attrs={
                'class': "form-control"
            }),
        }

    # Définir automatiquement un rôle lors de l'inscription (optionnel)
    def save(self, commit=True):
        """
        Cette méthode permet d'ajouter une logique personnalisée
        lors de la création d'un utilisateur.
        Par exemple, assigner automatiquement un rôle.
        """
        user = super().save(commit=False)
        user.role = "participant"  # Définir le rôle par défaut

        if commit:
            user.save()

        return user
