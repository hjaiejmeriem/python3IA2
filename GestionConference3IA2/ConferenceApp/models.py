from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
import uuid

# -------------------------------------------------------------------
# Fonction qui génère un identifiant unique pour les soumissions.
# Le format sera par exemple : SUB12EF78A2 (SUB + 8 caractères aléatoires)
# -------------------------------------------------------------------
def generate_submission_id():
    return "SUB" + uuid.uuid4().hex[:8].upper()


# ===================================================================
#   MODEL : CONFERENCE
# ===================================================================
class Conference(models.Model):
    # Identifiant automatique pour chaque conférence
    conference_id = models.AutoField(primary_key=True)

    # Nom de la conférence
    name = models.CharField(max_length=255)

    # Liste déroulante (choice field) pour la thématique
    THEME = [
        ("IA", "Computer science & IA"),
        ("SE", "Science & Engineering"),
        ("SC", "Social sciences"),
    ]
    theme = models.CharField(max_length=255, choices=THEME)

    # Lieu de la conférence
    location = models.CharField(max_length=50)

    # Description limitée à 300 caractères
    description = models.TextField(
        validators=[
            MaxLengthValidator(300, "Vous avez utilisé la limite maximale de texte autorisé.")
        ]
    )

    # Dates de début et fin
    start_date = models.DateField()
    end_date = models.DateField()

    # Champs automatiques : date de création et de mise à jour
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Représentation dans l'admin et Django shell
    def __str__(self):
        return f"Conférence : {self.name}"

    # -------------------------------------------------------------------
    # VALIDATION : empêcher que la date de début soit après la date de fin
    # clean() est exécutée automatiquement dans ModelForm ou admin
    # -------------------------------------------------------------------
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")


# ===================================================================
#   MODEL : SUBMISSION
# ===================================================================
class Submission(models.Model):

    # Identifiant unique NON modifiable par l'utilisateur
    submission_id = models.CharField(
        max_length=255,
        primary_key=True,
        unique=True,
        editable=False
    )

    # Champs principaux de la soumission
    title = models.CharField(max_length=50)
    abstract = models.TextField()
    keywords = models.TextField()

    # Upload du fichier PDF de l’article
    paper = models.FileField(upload_to="papers/")

    # Statut de la soumission
    STATUS = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS)

    # Est-ce que l'auteur a payé les frais ?
    payed = models.BooleanField(default=False)

    # Dates automatiques
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Lien vers l'utilisateur (auteur de la soumission)
    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="submissions"  # Permet user.submissions.all()
    )

    # Lien vers la conférence associée
    conference = models.ForeignKey(
        Conference,
        on_delete=models.CASCADE,
        related_name="submissions"  # Permet conference.submissions.all()
    )

    # -------------------------------------------------------------------
    # save() personnalisé pour générer automatiquement un ID unique
    # avant d'enregistrer dans la base de données
    # -------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # Si l'ID n'existe pas, on le génère
        if not self.submission_id:
            newid = generate_submission_id()

            # Vérifier qu'il n'existe pas déjà (rare mais possible)
            while Submission.objects.filter(submission_id=newid).exists():
                newid = generate_submission_id()

            self.submission_id = newid
        
        # Appel de la méthode save() normale de Django
        super().save(*args, **kwargs)
