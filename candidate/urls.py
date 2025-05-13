from django.urls import path
from candidate import views

urlpatterns = [
    path('candidate-dashboard/',views.candidate_dashboard,name='candidate_dashboard'),
    path('my-job-list/',views.myJobListviews,name='myJobListviews'),
    path('apply-for-job/<int:pk>/',views.applyforjob,name='applyforjob'),
]  