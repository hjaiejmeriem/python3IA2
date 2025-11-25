from django.db import models
from django.contrib.auth.models import AbstractUser  # On hérite du modèle utilisateur par défaut pour personnaliser les champs
from django.core.exceptions import ValidationError     # Pour lever des erreurs personnalisées
from django.core.validators import RegexValidator     # Pour valider des champs avec des expressions régulières
import uuid                                           # Pour générer des identifiants uniques


# ============================
# FONCTION : générer un ID utilisateur unique
# ============================
def generate_user_id():
    # Renvoie un ID au format USERXXXX (4 caractères aléatoires en majuscules)
    return "USER" + uuid.uuid4().hex[:4].upper()
    # ⚠️ Note : 4 caractères aléatoires peuvent être courts si beaucoup d'utilisateurs

# ============================
# FONCTION : validation des emails
# ============================
def verify_email(email):
    # Liste des domaines autorisés (emails universitaires privés)
    domaines = ["esprit.tn", "seasame.com", "tek.tn", "central.net"]
    
    # Récupère le domaine après le "@" dans l'email
    email_domaine = email.split("@")[1]

    # Vérifie si le domaine est autorisé
    if email_domaine not in domaines:
        raise ValidationError("L'email est invalide et doit appartenir à un domaine universitaire privé")

# ============================
# VALIDATEUR POUR LES NOMS
# ============================
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',  # Autorise uniquement lettres, espaces et tirets
    message="Ce champ ne doit contenir que des lettres et des espaces"
)


# ============================
# MODELE UTILISATEUR PERSONNALISE
# ============================
class User(AbstractUser):
    # ID unique de l'utilisateur, clé primaire
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)

    # Nom et prénom avec validation
    first_name = models.CharField(max_length=255, validators=[name_validator])
    last_name = models.CharField(max_length=255, validators=[name_validator])

    # Choix possibles pour le rôle de l'utilisateur
    ROLE = [
        ("particpant", "participant"),     # ❌ Note : "particpant" est mal orthographié, devrait être "participant"
        ("commitee", "organizing commitee member"),  # ❌ Note : "commitee" est mal orthographié, devrait être "committee"
    ]

    # Champ rôle avec valeur par défaut "participant"
    role = models.CharField(max_length=255, choices=ROLE, default="participant")

    # Affiliation universitaire ou organisation
    affiliation = models.CharField(max_length=255)

    # Email unique avec validation du domaine
    email = models.EmailField(unique=True, validators=[verify_email])

    # Nationalité de l'utilisateur
    nationality = models.CharField(max_length=255)

    # Dates de création et de mise à jour
    created_at = models.DateTimeField(auto_now_add=True)  # rempli automatiquement à la création
    update_at = models.DateTimeField(auto_now=True)      # mis à jour automatiquement à chaque modification

    # ============================
    # SAUVEGARDE PERSONNALISEE
    # ============================
    def save(self, *args, **kwargs):
        """
        Si l'utilisateur n'a pas d'user_id, on en génère un avant de sauvegarder.
        Cela garantit que chaque utilisateur a un ID unique au format USERXXXX.
        """
        if not self.user_id:
            newid = generate_user_id()
            # Vérifie que l'ID généré n'existe pas déjà dans la base
            while User.objects.filter(user_id=newid).exists():
                newid = generate_user_id()
            self.user_id = newid
        
        # Appelle la méthode save() originale pour sauvegarder l'objet
        super().save(*args, **kwargs)


# ============================
# MODELE COMITÉ ORGANISATEUR
# ============================
class OrganizingCommittee(models.Model):
    # Rôle du membre dans le comité (chair, co-chair, member)
    commitee_role = models.CharField(
        max_length=255,
        choices=[
            ("chair", "chair"),
            ("co-chair", "co-chair"),
            ("member", "member"),
        ]
    )

    # Date de début de participation au comité
    join_date = models.DateField()

    # Dates de création et mise à jour du record
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Relation avec l'utilisateur (clé étrangère vers le modèle User)
    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="committees"  # Permet d'accéder aux comités d'un utilisateur via user.committees
    )

    # Relation avec la conférence (clé étrangère vers le modèle Conference)
    conference = models.ForeignKey(
        "ConferenceApp.Conference",
        on_delete=models.CASCADE,
        related_name="committees"  # Permet d'accéder aux comités d'une conférence via conference.committees
    )
