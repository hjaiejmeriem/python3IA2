from django.shortcuts import render, redirect  # render pour afficher les templates, redirect pour rediriger après une action
from .forms import UserRegisterForm             # le formulaire d'inscription personnalisé
from django.contrib.auth import logout          # fonction pour déconnecter un utilisateur


# ============================
# VUE : Inscription utilisateur
# ============================
def register(req):
    """
    Permet à un nouvel utilisateur de s'inscrire via le formulaire UserRegisterForm.
    """
    if req.method == "POST":
        # Si le formulaire est soumis
        form = UserRegisterForm(req.POST)  # On récupère les données POST dans le formulaire
        if form.is_valid():                # Vérifie que le formulaire est valide (tous les champs ok)
            form.save()                    # Sauvegarde l'utilisateur dans la base de données
            return redirect("login")       # Redirige vers la page de connexion après l'inscription
    else:
        # Si c'est une requête GET (simple affichage du formulaire)
        form = UserRegisterForm()

    # Affiche le template 'register.html' avec le formulaire
    return render(req, 'register.html', {"form": form})


# ============================
# VUE : Déconnexion utilisateur
# ============================
def logout_view(req):
    """
    Déconnecte l'utilisateur actuel et le redirige vers la page de connexion.
    """
    logout(req)           # Déconnecte l'utilisateur (supprime sa session)
    return redirect("login")  # Redirige vers la page de login
