from django.apps import AppConfig

class ConferenceappConfig(AppConfig):
    # Indique à Django d'utiliser un entier 64 bits auto-incrémenté
    # pour les id (clé primaire) par défaut
    default_auto_field = 'django.db.models.BigAutoField'

    # Le nom de l'application (doit correspondre au nom du dossier)
    name = 'ConferenceApp'
