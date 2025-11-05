# Care Mate

A Django 5 + Channels project for a healthcare platform with user accounts, profiles, real‑time chat, AI assistant, dashboards, and a REST API (with Swagger/Redoc). Uses PostgreSQL, Redis, Celery, DRF, and JWT.

## Tech Stack
- **Backend**: Django 5, Django Channels, ASGI (Daphne)
- **API**: Django REST Framework, drf-yasg (Swagger/Redoc)
- **Auth**: Custom user model, SimpleJWT (tokens)
- **Async**: Celery, Redis (broker + result backend), WebSockets
- **DB**: PostgreSQL
- **Templates/Static**: Django templates under `template/`, static under `static/`

## Project Structure
- **manage.py**
- **src/**: Django project (settings, urls, asgi/wsgi, celery)
- **user_account/**: registration, login, email verification, password reset, API
- **profile_users/**: patient profile, appointments, API
- **dashboard/**: doctor dashboard, scheduling, reporting, API
- **home/**: landing, search, doctor detail, API and context processor
- **ai_assistant/**: AI chat views and API
- **chat/**: real‑time chat (Channels) views and rooms
- **template/**: templates grouped by app
- **static/**: static assets (images, js, media)

## Features
- **User accounts**: signup/login/logout, password reset, email verification
- **Profiles**: patient profile management
- **Dashboard**: doctor dashboard, appointment management, scheduling, reporting
- **Search & detail**: browse/search doctors, detail pages
- **Chat**: real‑time user chat via WebSockets
- **AI Assistant**: chat UI and REST endpoints; integrates with Google Generative AI
- **API Docs**: Swagger at `/swagger/`, Redoc at `/redoc/`

## Requirements
- Python 3.11+ (recommended)
- PostgreSQL 13+
- Redis 6+

## Environment Variables
Create a `.env` file in the project root (same folder as `manage.py`). The project already loads it with `python-dotenv`.

Required:
- `SECRET_KEY` — Django secret key
- `EMAIL_HOST_USER` — SMTP user (e.g., Gmail address)
- `EMAIL_HOST_PASSWORD` — SMTP app password

Optional (with defaults in code):
- `REDIS_URL` — e.g., `redis://127.0.0.1:6379/1`
- `GEMINI_API_KEY` — for AI assistant features

Note: Database settings are currently hardcoded in `src/settings.py` for local dev:
- NAME: `health`, USER: `ahmed`, PASSWORD: `programming`, HOST: `localhost`, PORT: `5432`
Adjust these in `src/settings.py` for your environment.

## Setup
1) Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Start PostgreSQL and create the database/user (if needed)
```bash
# Example (adapt to your env)
createdb health
# ensure user `ahmed` with password `programming` exists or change settings
```

4) Apply migrations and create a superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

5) Run Redis
```bash
redis-server
```

## Running the App
- Django dev server (ASGI):
```bash
python manage.py runserver
```

- Celery worker (async tasks):
```bash
celery -A src worker -l info
```

- Optional ASGI server (Daphne):
```bash
daphne -b 0.0.0.0 -p 8000 src.asgi:application
```

## URLs
- App home: `/`
- Admin: `/admin/`
- Accounts: `/account/`
- Profiles: `/profile/`
- Dashboard: `/dashboard/`
- Chat: `/chat/`
- AI Assistant: `/ai/`
- API Docs (Swagger): `/swagger/`
- API Docs (Redoc): `/redoc/`

## REST & Auth
- DRF enabled with throttling. JWT via SimpleJWT is included; ensure clients use Bearer tokens for protected endpoints.
- Swagger/Redoc are available in DEBUG.

## Static & Media
- Static URL: `/static/`
- STATICFILES_DIRS points to `static/`
- Media URL: `/media/` served from `static/media/` in development

## Email
Configured for SMTP (Gmail):
- Host: `smtp.gmail.com`, Port: `587`, TLS: `True`
- Provide `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`

## Troubleshooting
- Missing env vars: ensure `.env` exists and contains required keys.
- DB connection errors: verify PostgreSQL is running and `src/settings.py` DB credentials match.
- Redis/Channels errors: ensure Redis is running and `REDIS_URL` is correct.
- WebSockets: ASGI is configured; `runserver` uses ASGI in modern Django, but using Daphne/uvicorn can help in complex setups.
- Migrations: run `python manage.py makemigrations` then `migrate` if you add models.

## Development Tips
- Custom user model: `AUTH_USER_MODEL = 'user_account.User'` (set at project start).
- Throttling and JWT settings are defined in `src/settings.py`.
- Celery app lives in `src/celery.py` and auto-discovers tasks in installed apps.

## License
MIT (or update accordingly).
