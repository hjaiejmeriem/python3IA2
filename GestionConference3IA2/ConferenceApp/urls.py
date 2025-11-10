from django.urls import path
from . import views
from .views import *
urlpatterns =[
 #path("liste/", views.list_conferences, name="liste_conferences"),
    path("liste/",ConferenceList.as_view(),name="liste_conferences"),
    path("<int:pk>/",ConferenceDetails.as_view(),name="conference_details"),
    path("add/",ConferenceCreate.as_view(),name="conference_add"),
    path("edit/<int:pk>/",ConferenceUpdate.as_view(),name="conference_update"),
    path("delete/<int:pk>/",ConferenceDelete.as_view(),name="conference_delete"),
    #to add
    # Submissions
    path('submissions/', ListSubmissionsView.as_view(), name='list_submissions'),
    path('submissions/add/', AddSubmissionView.as_view(), name='add_submission'),
    path('submissions/<str:pk>/', DetailSubmissionView.as_view(), name='detail_submission'),
    path('submissions/update/<str:pk>/', UpdateSubmission.as_view(), name='update_submission'),

    ]