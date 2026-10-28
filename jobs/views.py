from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .serializers import JobSerializer
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy

from .forms import JobForm
from .models import Application, Job

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from .permissions import IsEmployer, IsJobOwner
from .serializers import JobCreateSerializer
from .permissions import IsSeeker
from .serializers import ApplicationCreateSerializer
from .serializers import ApplicationSerializer


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login/'
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employer'


class JobOwnerRequiredMixin(EmployerRequiredMixin):
    def test_func(self):
        if not super().test_func():
            return False
        return self.get_object().posted_by == self.request.user


# Create your views here.
class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        location = self.request.GET.get('location', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(company_name__icontains=query)
                | Q(description__icontains=query)
                | Q(location__icontains=query)
            )

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['already_Applied'] = Application.objects.filter(
            job=self.object, applicant=self.request.user
            ).exists()
        return context
        
class JobCreateView(EmployerRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('jobs:job_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class JobUpdateView(JobOwnerRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('jobs:job_list')

class JobDeleteView(JobOwnerRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('jobs:job_list')

@login_required
@require_POST
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    Application.objects.get_or_create(job=job, applicant=request.user)
    return redirect('jobs:job_detail', pk=pk)


@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        raise PermissionDenied

    jobs = Job.objects.filter(posted_by=request.user).prefetch_related('application_set')
    context = {
        'jobs': jobs,
    }
    return render(request, 'employer_dashboard.html', context)


@login_required
def seeker_dashboard(request):
    if request.user.role != 'seeker':
        raise PermissionDenied

    applications = Application.objects.filter(applicant=request.user).select_related('job')
    context = {
        'applications': applications,
    }
    return render(request, 'seeker_dashboard.html', context)


class JobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.select_related("posted_by").all()

class JobPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class JobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer
    pagination_class = JobPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "title",
        "company_name",
        "description",
        "location",
    ]

    ordering_fields = [
        "date_posted",
        "salary",
        "title",
    ]

    ordering = ["-date_posted"]

    def get_queryset(self):
        return Job.objects.select_related("posted_by").all()


class JobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class JobManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobCreateSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsJobOwner]

    def get_queryset(self):
        return Job.objects.select_related("posted_by").all()


class JobApplicationCreateAPIView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsSeeker]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)



class ApplicationListAPIView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination
    
    def get_queryset(self):
        user = self.request.user

        if user.role == "seeker":
            return Application.objects.filter(
                applicant=user
        ).select_related("job", "applicant").order_by("-date_applied", "-id")

        if user.role == "employer":
            return Application.objects.filter(
                job__posted_by=user
            ).select_related("job", "applicant").order_by("-date_applied", "-id")

        return Application.objects.none()










