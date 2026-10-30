# Django Job Portal

A full-stack Job Portal built with **Python, Django and Django REST Framework**. The platform connects job seekers with employers, allowing employers to publish and manage job listings while job seekers can search for opportunities and submit applications.

**Live Application:** https://django-job-portal-niln.onrender.com/

**GitHub Repository:** https://github.com/theriyachauhan17-del/Django-Job-Portal

---

## Features

### Website Features
- Custom Django user model with Job Seeker and Employer roles.
- User registration, login and logout.
- Job search by keyword and location.
- Employer dashboard for managing job listings.
- Job seeker dashboard for tracking applications.
- Job application submission.
- Duplicate application prevention.
- Responsive HTML templates.

### REST API Features
- List and retrieve job listings.
- Search, ordering and pagination.
- Employer-only job creation.
- Job-owner-only update and deletion.
- Job seeker application submission.
- Role-based application listing.
- Authentication and permission validation.
- JSON request and response handling.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Backend programming |
| Django 6.1.2 | Web framework |
| Django REST Framework 3.18.3 | REST API development |
| PostgreSQL | Production database |
| Supabase | Managed PostgreSQL database |
| SQLite | Local development, if configured |
| HTML and CSS | Frontend |
| Gunicorn | Production application server |
| WhiteNoise | Static file serving |
| Render | Application deployment |
| Postman | API testing |
| Git and GitHub | Version control |

## Project Structure

```text
Django-Job-Portal/
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── jobs/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests.py
│
├── jobportal/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── build.sh
├── .gitignore
└── README.md
```

## Installation and Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/theriyachauhan17-del/Django-Job-Portal.git
cd Django-Job-Portal
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Configure the environment variables required by your Django settings.

Typical production settings include:

```text
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain
DATABASE_URL=your-database-connection-url
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain
```

Use your own local database configuration for development. Never commit real passwords, secret keys or database URLs to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## REST API Documentation

**Base URL:**

```text
https://django-job-portal-niln.onrender.com
```

### Job APIs

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/jobs/` | List jobs | Public |
| POST | `/api/jobs/create/` | Create a job | Employer |
| GET | `/api/jobs/<id>/manage/` | Retrieve a managed job | Job owner |
| PUT | `/api/jobs/<id>/manage/` | Replace job details | Job owner |
| PATCH | `/api/jobs/<id>/manage/` | Partially update a job | Job owner |
| DELETE | `/api/jobs/<id>/manage/` | Delete a job | Job owner |

### Application APIs

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/applications/` | Submit a job application | Job Seeker |
| GET | `/api/applications/list/` | List permitted applications | Authenticated user |

### Example: Create a Job

**Request**

```http
POST /api/jobs/create/
```

**JSON Body**

```json
{
    "title": "Junior Python Developer",
    "company_name": "Demo Tech",
    "description": "Develop and maintain Django REST APIs.",
    "location": "Remote",
    "salary": "45000.00"
}
```

**Authentication:** Employer account with the required permissions.

### Example: Apply for a Job

**Request**

```http
POST /api/applications/
```

**JSON Body**

```json
{
    "job": 1
}
```

**Authentication:** Job Seeker account.

### Authentication and Permissions

The API uses authenticated requests and role-based permissions.

- **Employer:** Can create jobs.
- **Job Owner:** Can retrieve, update and delete their own jobs.
- **Job Seeker:** Can submit job applications.
- **Authenticated User:** Can view applications permitted by their account role.

Use the authentication method configured by the application when testing protected endpoints in Postman.

## API Testing with Postman

The following production API operations were tested successfully:

| Operation | Method | Result |
|---|---|---|
| List jobs | GET | 200 OK |
| Create job | POST | 201 Created |
| Submit application | POST | 201 Created |
| List applications | GET | 200 OK |
| Partially update job | PATCH | 200 OK |
| Replace job | PUT | 200 OK |
| Delete job | DELETE | 204 No Content |

## Automated Testing

Run the test suite:

```bash
python manage.py test
```

The project previously passed **31 automated tests**. Run the suite again to confirm the current result.

## Deployment

The application is deployed using:

- **Render:** Django web application hosting.
- **Supabase:** PostgreSQL database hosting.
- **Gunicorn:** Production WSGI server.
- **WhiteNoise:** Static file serving.

Live application:

https://django-job-portal-niln.onrender.com/

Django Admin:

https://django-job-portal-niln.onrender.com/admin/

Production credentials and database connection details are not included in this repository.

## Screenshots

Add genuine screenshots of your running application and API tests in a `screenshots/` directory.

Suggested screenshots:

- Homepage and job listings.
- Job details.
- Employer dashboard.
- Job seeker dashboard.
- Django Admin.
- Successful Postman API requests.

## Future Improvements

- Add automated API documentation using Swagger or OpenAPI.
- Add email notifications for job applications.
- Improve automated test coverage.
- Add CI/CD integration.
- Improve frontend user experience.
- Add advanced filtering and job recommendations.

## Author

**Riya Chauhan**

GitHub: https://github.com/theriyachauhan17-del

---

*Developed as a portfolio project to demonstrate Python, Django, Django REST Framework, PostgreSQL, authentication, API development, testing and deployment skills.*