# VisaPilot Global Mobility Platform (Foundation)

This repository now contains a production-oriented foundation for a modular **Global Mobility Intelligence Platform** with major domains:

- Visa Assistant
- Job Relocation
- Study Placement
- Immigration Analytics

## Stack

- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Queue/Cache: Celery + Redis
- Auth: JWT-ready (SimpleJWT installed)
- Deployment: Docker + Gunicorn + Nginx reverse proxy template

## Project Structure

```text
config/
apps/
  accounts/
  visa/
  relocation/
  study/
  analytics/
  documents/
  ai_assistant/
  payments/
  notifications/
  admin_portal/
  compliance/
```

Each app includes:

- `models.py`
- `serializers.py`
- `views.py`
- `services.py`
- `permissions.py`
- `urls.py`
- `tests.py`

Business logic is intentionally designed to live in service classes (for example `EligibilityEngine` in `apps/visa/services.py`) instead of view classes.

## API Namespaces

The following base routes are wired in `config/urls.py`:

- `/api/v1/auth/`
- `/api/v1/visa/`
- `/api/v1/documents/`
- `/api/v1/ai/`
- `/api/v1/relocation/`
- `/api/v1/study/`
- `/api/v1/analytics/`
- `/api/v1/payments/`
- `/api/v1/admin/`
- `/api/v1/notifications/`
- `/api/v1/compliance/`

## Key Implemented Foundations

- Custom user model with role support and organization membership (`accounts`).
- Required role and organization type enums.
- Visa module core entities and rule-based eligibility service.
- Document management base models with private-by-default files.
- AI assistant models and mandatory immigration disclaimer wrapper.
- Relocation, study placement, analytics, payment/subscription, notification, admin log, and compliance policy base entities.

## Quick Start

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Docker

```bash
docker compose up --build
```

## Next Build Steps

1. Add migrations and seed data (visa programs, countries, prompt templates).
2. Implement JWT login/register/refresh endpoints.
3. Add granular RBAC permissions mapped to role + organization context.
4. Implement payment provider adapters (Paystack/Flutterwave/Stripe).
5. Integrate object storage + malware scanning for uploads.
6. Add event tracking instrumentation and analytics dashboards.
7. Expand service-level tests to meet 80%+ logic coverage.
