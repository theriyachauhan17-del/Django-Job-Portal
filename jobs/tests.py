from rest_framework.test import APITestCase
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


class JobListAPITests(APITestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username="api-employer",
            email="api-employer@example.com",
            password="StrongPass123!",
            role="employer",
        )

        for number in range(1, 7):
            Job.objects.create(
                title=f"Python Developer {number}",
                company_name=f"Company {number}",
                description=f"Python backend role {number}",
                location="Remote",
                salary=50000 + number * 1000,
                posted_by=self.employer,
            )

        self.url = reverse("jobs:api_job_list")

    def test_list_jobs_returns_200_and_job_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 6)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIn("title", response.data["results"][0])
        self.assertIn("company_name", response.data["results"][0])

    def test_search_returns_matching_jobs(self):
        response = self.client.get(self.url, {"search": "Company 1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["company_name"],
            "Company 1",
        )

    def test_pagination_returns_remaining_job(self):
        response = self.client.get(
            self.url,
            {"page": 2, "page_size": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 6)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIsNotNone(response.data["previous"])

    def test_invalid_page_returns_404(self):
        response = self.client.get(
            self.url,
            {"page": 999, "page_size": 2},
        )

        self.assertEqual(response.status_code, 404)


class JobCreateAPITests(APITestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username="create-api-employer",
            password="StrongPass123!",
            role="employer",
        )

        self.seeker = CustomUser.objects.create_user(
            username="create-api-seeker",
            password="StrongPass123!",
            role="seeker",
        )

        self.url = reverse("jobs:api_job_create")

        self.valid_payload = {
            "title": "Python Developer",
            "company_name": "Example Tech",
            "description": "Develop and maintain Django REST APIs.",
            "location": "Remote",
            "salary": "60000.00",
        }

    def test_employer_can_create_job(self):
        self.client.force_authenticate(user=self.employer)

        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Job.objects.count(), 1)

        job = Job.objects.get()
        self.assertEqual(job.posted_by, self.employer)
        self.assertEqual(job.title, "Python Developer")

    def test_seeker_cannot_create_job(self):
        self.client.force_authenticate(user=self.seeker)

        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Job.objects.count(), 0)

    def test_anonymous_user_cannot_create_job(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Job.objects.count(), 0)


class JobOwnershipAPITests(APITestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username="owner-employer",
            password="StrongPass123!",
            role="employer",
        )
        self.other_employer = CustomUser.objects.create_user(
            username="other-employer",
            password="StrongPass123!",
            role="employer",
        )

        self.job = Job.objects.create(
            title="Python Developer",
            company_name="Example Tech",
            description="Build Django applications.",
            location="Remote",
            salary="60000.00",
            posted_by=self.employer,
        )

        self.url = reverse(
            "jobs:api_job_manage",
            kwargs={"pk": self.job.pk},
        )

    def test_owner_can_update_own_job(self):
        self.client.force_authenticate(user=self.employer)

        response = self.client.patch(
            self.url,
            {"title": "Senior Python Developer"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "Senior Python Developer")

    def test_other_employer_cannot_update_job(self):
        self.client.force_authenticate(user=self.other_employer)

        response = self.client.patch(
            self.url,
            {"title": "Unauthorized Change"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "Python Developer")

    def test_owner_can_delete_own_job(self):
        self.client.force_authenticate(user=self.employer)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Job.objects.filter(pk=self.job.pk).exists())


class JobApplicationAPITests(APITestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            username="application-employer",
            password="StrongPass123!",
            role="employer",
        )
        self.seeker = CustomUser.objects.create_user(
            username="application-seeker",
            password="StrongPass123!",
            role="seeker",
        )

        self.job = Job.objects.create(
            title="Python Developer",
            company_name="Example Tech",
            description="Develop Django REST APIs.",
            location="Remote",
            salary="60000.00",
            posted_by=self.employer,
        )

        self.url = reverse("jobs:api_application_create")

    def test_seeker_can_apply_for_job(self):
        self.client.force_authenticate(user=self.seeker)

        response = self.client.post(
            self.url,
            {"job": self.job.pk},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        application = Application.objects.get()
        self.assertEqual(application.applicant, self.seeker)
        self.assertEqual(application.job, self.job)

    def test_seeker_cannot_apply_twice(self):
        self.client.force_authenticate(user=self.seeker)

        first_response = self.client.post(
            self.url,
            {"job": self.job.pk},
            format="json",
        )
        second_response = self.client.post(
            self.url,
            {"job": self.job.pk},
            format="json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(Application.objects.count(), 1)

    def test_employer_cannot_apply_for_job(self):
        self.client.force_authenticate(user=self.employer)

        response = self.client.post(
            self.url,
            {"job": self.job.pk},
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Application.objects.count(), 0)

    def test_anonymous_user_cannot_apply(self):
        response = self.client.post(
            self.url,
            {"job": self.job.pk},
            format="json",
        )

        self.assertIn(response.status_code, [401, 403])
        self.assertEqual(Application.objects.count(), 0)

