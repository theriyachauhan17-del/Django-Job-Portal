# Django Job Portal

A job portal built with Django and Django REST Framework that connects job seekers with employers. Employers can publish and manage job listings, while job seekers can search for jobs and track their applications.

## Features

### Website
- Custom user model with job seeker and employer roles
- User registration, login, and logout
- Job search by keyword and location
- Employer dashboard to manage job listings and view applicants
- Job seeker dashboard to track applications
- Duplicate application prevention
- Responsive HTML templates

### REST API
- Public job listing endpoint with search, ordering, and pagination
- Employer-only job creation
- Owner-only job updates and deletion
- Job seeker application submission
- Duplicate application prevention
- Role-based application listing
- Authentication and permission checks

## Technology Stack

- Python
- Django 6.1.2
- Django REST Framework 3.18.3
- SQLite for local development
- HTML and CSS
- Git and GitHub

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/theriyachauhan17-del/Django-Job-Portal.git
cd Django-Job-Portal
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run database migrations

```powershell
python manage.py migrate
```

### 5. Create an administrator

```powershell
python manage.py createsuperuser
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/jobs/` | List and search jobs |
| POST | `/api/jobs/create/` | Create a job as an employer |
| GET | `/api/jobs/<id>/manage/` | Retrieve a managed job |
| PATCH | `/api/jobs/<id>/manage/` | Update an owned job |
| DELETE | `/api/jobs/<id>/manage/` | Delete an owned job |
| POST | `/api/applications/` | Apply for a job as a seeker |
| GET | `/api/applications/list/` | List applications permitted for the logged-in user |

Protected endpoints require authentication and appropriate role or ownership permissions. Confirm the exact methods and permissions against the current URL configuration and views.

## Testing

Run the complete test suite:

```powershell
python manage.py test
```

The project currently has 31 automated tests covering website workflows, API functionality, authentication, permissions, and application handling.

## Screenshots

Add screenshots of the homepage, job details, employer dashboard, applications dashboard, and API responses in a `screenshots/` folder. Embed them here after capturing the actual running application.

## Security and Deployment

- Keep production secrets out of Git.
- Set `DJANGO_DEBUG=False` in production.
- Configure a private `DJANGO_SECRET_KEY` and appropriate `DJANGO_ALLOWED_HOSTS`.
- Use HTTPS and review secure-cookie and API authentication settings.
- Configure production database and static-file serving.
- Run Django's deployment checks before launch.

SQLite and the console email backend are intended for development; configure production alternatives as needed.

## Project Structure

```text
accounts/    Custom user model and account functionality
jobs/        Job and application models, views, serializers, permissions, and tests
jobportal/   Django settings and URL configuration
manage.py    Django management utility
requirements.txt
README.md
```

## Author

**Riya Chauhan**

GitHub: [@theriyachauhan17-del](https://github.com/theriyachauhan17-del)