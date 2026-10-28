# jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('my-applications/', views.seeker_dashboard, name='seeker_dashboard'),
    path('new/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('new/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('<int:pk>/apply/', views.apply_to_job, name='apply_to_job'),

    # New REST API route
    path('api/jobs/', views.JobListAPIView.as_view(), name='api_job_list'),
    path("api/jobs/create/", views.JobCreateAPIView.as_view(), name="api_job_create"),
    path("api/jobs/<int:pk>/manage/", views.JobManageAPIView.as_view(), name="api_job_manage"),
    path("api/applications/", views.JobApplicationCreateAPIView.as_view(), name="api_application_create"),
    path("api/applications/list/", views.ApplicationListAPIView.as_view(), name="api_application_list"),
]