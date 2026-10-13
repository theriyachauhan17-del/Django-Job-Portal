from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from jobs.models import Application, Job


class EmployerAccessTests(TestCase):
    def setUp(self):
        self.seeker = CustomUser.objects.create_user(
            username='jobseeker',
            email='seeker@example.com',
            password='StrongPass123!',
            role='seeker',
        )
        self.employer = CustomUser.objects.create_user(
            username='jobemployer',
            email='employer@example.com',
            password='StrongPass123!',
            role='employer',
        )
        self.job = Job.objects.create(
            title='Python Developer',
            company_name='Acme',
            description='Build backend systems.',
            location='Remote',
            salary=90000,
            posted_by=self.employer,
        )
        self.application = Application.objects.create(
            job=self.job,
            applicant=self.seeker,
        )

    def test_seeker_cannot_access_job_create_page(self):
        self.client.force_login(self.seeker)
        response = self.client.get(reverse('jobs:job_create'))
        self.assertEqual(response.status_code, 403)

    def test_employer_can_access_job_create_page(self):
        self.client.force_login(self.employer)
        response = self.client.get(reverse('jobs:job_create'))
        self.assertEqual(response.status_code, 200)

    def test_employer_dashboard_lists_owned_jobs_and_applicants(self):
        self.client.force_login(self.employer)
        response = self.client.get(reverse('jobs:employer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.seeker.username)

    def test_seeker_cannot_access_employer_dashboard(self):
        self.client.force_login(self.seeker)
        response = self.client.get(reverse('jobs:employer_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_seeker_dashboard_lists_applied_jobs(self):
        self.client.force_login(self.seeker)
        response = self.client.get(reverse('jobs:seeker_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)
        self.assertContains(response, self.seeker.username)

    def test_employer_cannot_access_seeker_dashboard(self):
        self.client.force_login(self.employer)
        response = self.client.get(reverse('jobs:seeker_dashboard'))
        self.assertEqual(response.status_code, 403)


class JobApplicationActionTests(TestCase):
    def setUp(self):
        self.seeker = CustomUser.objects.create_user(
            username='applicant',
            email='applicant@example.com',
            password='StrongPass123!',
            role='seeker',
        )
        self.employer = CustomUser.objects.create_user(
            username='company',
            email='company@example.com',
            password='StrongPass123!',
            role='employer',
        )
        self.job = Job.objects.create(
            title='Backend Developer',
            company_name='Example Co',
            description='Build web services.',
            location='Remote',
            salary=85000,
            posted_by=self.employer,
        )
        self.apply_url = reverse('jobs:apply_to_job', args=[self.job.pk])

    def test_get_does_not_apply_to_job(self):
        self.client.force_login(self.seeker)

        response = self.client.get(self.apply_url)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Application.objects.filter(job=self.job, applicant=self.seeker).exists())

    def test_post_applies_to_job(self):
        self.client.force_login(self.seeker)

        response = self.client.post(self.apply_url)

        self.assertRedirects(response, reverse('jobs:job_detail', args=[self.job.pk]))
        self.assertTrue(Application.objects.filter(job=self.job, applicant=self.seeker).exists())

    def test_repeated_post_does_not_duplicate_application(self):
        self.client.force_login(self.seeker)

        self.client.post(self.apply_url)
        self.client.post(self.apply_url)

        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)


class JobSearchTests(TestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username='search-employer',
            email='search-employer@example.com',
            password='StrongPass123!',
            role='employer',
        )
        self.remote_job = Job.objects.create(
            title='Python Developer',
            company_name='Northstar',
            description='Build data services.',
            location='Remote',
            salary=90000,
            posted_by=self.employer,
        )
        self.london_job = Job.objects.create(
            title='Python Developer',
            company_name='Southbank',
            description='Build web applications.',
            location='London',
            salary=85000,
            posted_by=self.employer,
        )

    def test_keyword_and_location_filters_are_combined(self):
        response = self.client.get(
            reverse('jobs:job_list'),
            {'q': 'Northstar', 'location': 'Remote'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.remote_job.title)
        self.assertContains(response, self.remote_job.company_name)
        self.assertNotContains(response, self.london_job.company_name)

    def test_search_matches_job_description(self):
        response = self.client.get(reverse('jobs:job_list'), {'q': 'data services'})

        self.assertContains(response, self.remote_job.company_name)
        self.assertNotContains(response, self.london_job.company_name)
