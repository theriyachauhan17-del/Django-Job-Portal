# Job Portal

A Django job portal with separate employer and job-seeker experiences. Employers can publish and manage listings; job seekers can search jobs and track their applications.

## Features

- Custom user roles for employers and job seekers
- Account registration, login, and logout
- Job listing search by keyword and location
- Employer dashboard for managing listings and viewing applicants
- Job seeker dashboard for tracking applications
- Protected job creation and owner-only job updates/deletion
- CSRF-protected job applications with duplicate-submission protection
- Responsive templates for the main workflows

## Technology

- Python
- Django 6.1
- SQLite for local development

## Setup on Windows

Run these commands from the folder that contains `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. Create an account through the signup page to try the job-seeker flow. To use employer features, create an account with the employer role.

If PowerShell blocks virtual-environment activation, run the commands using `..\venv\Scripts\python.exe` if you already have that environment, or configure your local PowerShell execution policy according to your organization's guidance.

## Environment Configuration

Local development defaults to `DEBUG=True`, `localhost` and `127.0.0.1`, and a development-only secret key. The development key must never be used in production.

Before deploying, configure these environment variables in your hosting provider:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`: a newly generated, private Django secret key
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames for the deployed site, such as `jobs.example.com`

Generate a secret key with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value directly into your hosting provider's secret/environment-variable settings. Do not commit the value or paste it into this README. When `DJANGO_DEBUG=False`, the application refuses to start without `DJANGO_SECRET_KEY`.

## Tests

Run the full test suite with:

```powershell
python manage.py test jobs accounts
```

The tests cover account signup, role-based access, dashboards, job applications, and keyword/location search.

## Screenshots

Capture screenshots from the running app so they reflect the current version. Useful screens for a portfolio README are:

- Homepage with search and job listings
- Job details with the Apply action
- Employer dashboard with a job listing
- My Applications dashboard
- Signup or login screen

On Windows, open each page in the browser and use `Win+Shift+S` to capture it. Save the images in a `screenshots` folder at the project root, using names such as `home.png`, `job-detail.png`, `employer-dashboard.png`, and `applications.png`. Then embed them here with Markdown, for example:

```markdown
![Job Portal homepage](screenshots/home.png)
```

Only include screenshots that do not expose personal information, email addresses, or real applicant data.

## Project Structure

```text
accounts/   Custom user model, authentication, and signup
jobs/       Job/application models, views, tests, and templates
jobportal/  Django project settings and root URL configuration
manage.py  Django management entry point
```

## Notes

SQLite is configured for local development. Before a public production deployment, use the hosting platform's recommended database and review Django's deployment checklist, HTTPS, static-file handling, backups, and logging.