from django.contrib import admin
from .models import Conference, Submission

# Personnalisation générale de l'admin Django
admin.site.site_title = "Gestion Conférence 25/26"
admin.site.site_header = "Gestion Conférences"
admin.site.index_title = "Django App Conférence"

# ---------------------------
# Inline : Submissions dans Conference
# ---------------------------
class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1  # une ligne vide par défaut
    readonly_fields = ("submission_date",)  # champ non modifiable


# ---------------------------
# Admin du modèle Conference
# ---------------------------
@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = ("name", "theme", "start_date", "end_date", "a")

    # Tri par date
    ordering = ("start_date",)

    # Filtres latéraux
    list_filter = ("theme",)

    # Recherche
    search_fields = ("description", "name")

    # Navigation temporelle
    date_hierarchy = "start_date"

    # Organisation du formulaire
    fieldsets = (
        ("Information générales", {
            "fields": ("conference_id", "name", "theme", "description")
        }),
        ("Informations logistiques", {
            "fields": ("location", "start_date", "end_date")
        })
    )

    # Champ non modifiable
    readonly_fields = ("conference_id",)

    # Méthode qui calcule la durée d'une conférence
    def a(self, objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date - objet.start_date).days
        return "RAS"
    a.short_description = "Duration (days)"

    # Inline pour afficher les Submissions liées
    inlines = [SubmissionInline]


# ---------------------------
# Actions personnalisées
# ---------------------------

@admin.action(description="Marquer comme payées")
def mark_as_payed(modeladmin, req, queryset):
    queryset.update(payed=True)

@admin.action(description="Marquer comme acceptées")
def mark_as_accepted(modeladmin, req, queryset):
    queryset.update(status="accepted")


# ---------------------------
# Admin du modèle Submission
# ---------------------------
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = ("title", "status", "payed", "submission_date")

    fieldsets = (
        ("Information générales", {
            "fields": ("title", "abstract", "keywords")
        }),
        ("Document", {
            "fields": ("paper", "user", "conference")
        }),
        ("Statut", {
            "fields": ("status", "payed")
        })
    )

    # Ajout des actions
    actions = [mark_as_payed, mark_as_accepted]
