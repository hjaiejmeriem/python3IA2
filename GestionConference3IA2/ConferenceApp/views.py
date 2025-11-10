from django.shortcuts import render
from .models import Conference, Submission
from django.views.generic import ListView , DetailView , CreateView,UpdateView,DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SubmissionForm
from django.core.exceptions import PermissionDenied

# Create your views here.


def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model= Conference
    template_name ="conferences/form.html"
    #fields = "__all__"
    form_class =ConferenceForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model =Conference
    template_name="conferences/form.html"
    #fields="__all__"
    form_class =ConferenceForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name ="conferences/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")
# views.py
class ListSubmissionsView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'submissions/list_submissions.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        # Retourne seulement les soumissions de l'utilisateur connecté
        return Submission.objects.filter(user=self.request.user).select_related('conference')
# views.py
class DetailSubmissionView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = 'submissions/detail_submission.html'
    context_object_name = 'submission'

    def get_queryset(self):
        # L'utilisateur ne peut voir que ses soumissions
        return Submission.objects.filter(user=self.request.user)
# views.py
class AddSubmissionView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submissions/submission_form.html'
    success_url = reverse_lazy('list_submissions')

    def form_valid(self, form):
        # Assigner automatiquement l'utilisateur connecté
        form.instance.user = self.request.user
        return super().form_valid(form)
# views.py
class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = SubmissionForm
    template_name = "submissions/update_submission.html"
    success_url = reverse_lazy("list_submissions")

    def get_queryset(self):
        # L'utilisateur ne peut modifier que ses propres soumissions
        return Submission.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        """Empêche modification si status est 'accepted' ou 'rejected'."""
        submission = super().get_object(queryset)
        if submission.status in ["accepted", "rejected"]:
            raise PermissionDenied("Cette soumission ne peut pas être modifiée.")
        return submission

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Rendre non modifiables certains champs
        for field in ["user", "conference"]:
            if field in form.fields:
                form.fields[field].disabled = True
        return form