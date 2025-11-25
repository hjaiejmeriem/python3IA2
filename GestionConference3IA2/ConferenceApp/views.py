from django.shortcuts import render
from .models import Conference, Submission
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm, SubmissionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# ============================================================
#   FONCTION SIMPLE : LISTE DES CONFÉRENCES
# ============================================================
def list_conferences(request):
    # Récupère toutes les conférences
    conferences_list = Conference.objects.all()

    # Envoie la liste au template liste.html
    return render(request, "conferences/liste.html", {"liste": conferences_list})


# ============================================================
#   LISTE DES CONFÉRENCES (version classe)
# ============================================================
class ConferenceList(ListView):
    model = Conference                      # Le modèle à afficher
    context_object_name = "liste"           # Nom utilisé dans le template
    template_name = "conferences/liste.html"


# ============================================================
#   DÉTAIL D'UNE CONFÉRENCE
# ============================================================
class ConferenceDetails(DetailView):
    model = Conference                      # récupère un objet Conference
    context_object_name = "conference"
    template_name = "conferences/details.html"


# ============================================================
#   AJOUTER UNE CONFÉRENCE (seulement si connecté)
# ============================================================
class ConferenceCreate(LoginRequiredMixin, CreateView):
    model = Conference
    template_name = "conferences/form.html"
    form_class = ConferenceForm             # Formulaire personnalisé
    success_url = reverse_lazy("liste_conferences")  # Après création, redirection


# ============================================================
#   MODIFIER UNE CONFÉRENCE (seulement si connecté)
# ============================================================
class ConferenceUpdate(LoginRequiredMixin, UpdateView):
    model = Conference
    template_name = "conferences/form.html"
    form_class = ConferenceForm
    success_url = reverse_lazy("liste_conferences")


# ============================================================
#   SUPPRIMER UNE CONFÉRENCE
# ============================================================
class ConferenceDelete(LoginRequiredMixin, DeleteView):
    model = Conference
    template_name = "conferences/conference_confirm_delete.html"
    success_url = reverse_lazy("liste_conferences")


# ============================================================
#   LISTE DES SUBMISSIONS DE L’UTILISATEUR CONNECTÉ
# ============================================================
class ListSubmissionsView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'submissions/list_submissions.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        """
        L'utilisateur ne doit voir QUE ses propres soumissions.
        select_related('conference') = optimisation des requêtes
        """
        return Submission.objects.filter(
            user=self.request.user
        ).select_related('conference')


# ============================================================
#   DÉTAIL D’UNE SUBMISSION
# ============================================================
class DetailSubmissionView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'submissions/detail_submission.html'
    context_object_name = 'submission'

    def get_queryset(self):
        """
        Empêche un utilisateur de voir les soumissions des autres.
        """
        return Submission.objects.filter(user=self.request.user)


# ============================================================
#   AJOUTER UNE SUBMISSION
# ============================================================
class AddSubmissionView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submissions/submission_form.html'
    success_url = reverse_lazy('list_submissions')

    def form_valid(self, form):
        """
        Assigne automatiquement l'utilisateur connecté à la soumission.
        Sans cela, Django demanderait un champ user dans le formulaire.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


# ============================================================
#   MODIFIER UNE SUBMISSION
# ============================================================
class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/update_submission.html"
    success_url = reverse_lazy("list_submissions")

    def get_queryset(self):
        """
        Empêche un utilisateur de modifier la soumission d'un autre.
        """
        return Submission.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        """
        Interdit la modification si la soumission est ACCEPTED ou REJECTED.
        """
        submission = super().get_object(queryset)
        if submission.status in ["accepted", "rejected"]:
            raise PermissionDenied("Cette soumission ne peut pas être modifiée.")
        return submission

    def get_form(self, form_class=None):
        """
        Rendre certains champs NON MODIFIABLES (user et conference).
        Très important pour la sécurité.
        """
        form = super().get_form(form_class)
        for field in ["user", "conference"]:
            if field in form.fields:
                form.fields[field].disabled = True
        return form
