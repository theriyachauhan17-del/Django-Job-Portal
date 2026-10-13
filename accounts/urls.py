# accounts/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='jobs:job_list'), name='logout'),
]