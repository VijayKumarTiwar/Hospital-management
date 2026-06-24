# Hospital / Clinic Management Backend

A Django REST Framework backend for a hospital/clinic management system, with
JWT authentication, role-based access (patient / doctor / admin), appointment
booking, a rule-based symptom-checker chatbot, and ML-based disease risk
prediction.

## Tech stack

- Django 6 + Django REST Framework
- PostgreSQL
- SimpleJWT (JWT auth)
- scikit-learn (risk prediction models)

## Project layout

```
config/          settings, root urls, wsgi/asgi
accounts/        custom User model (role: patient/doctor/admin), JWT auth
patients/        Patient profile, MedicalRecord
doctors/         Doctor profile, Specialization, DoctorAvailability
appointments/    Appointment booking + status workflow + signals
chatbot/         Rule-based symptom checker (keyword engine + chat history)
prediction/      ML risk prediction (diabetes, heart disease) via scikit-learn
notifications/   Per-user notification feed (used by appointments/reminders)
reminders/       Auto-scheduled appointment reminders + dispatch command
reports/         On-demand report generation (patient history, doctor stats)
dashboard/       Aggregate stats endpoints per role
```

## Setup

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# edit .env with your real SECRET_KEY and DB credentials
```

### 3. Create the PostgreSQL database

```bash
createdb hospital_db
# or in psql:
# CREATE DATABASE hospital_db;
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (for /admin/ and admin-role API access)

```bash
python manage.py createsuperuser
```
Note: the createsuperuser flow will set role=patient by default since that's
the model default. Promote yourself to admin in the Django shell:
```bash
python manage.py shell -c "
from accounts.models import User
u = User.objects.get(email='you@example.com')
u.role = User.Role.ADMIN
u.is_staff = True
u.is_superuser = True
u.save()
"
```

### 6. Train the ML risk-prediction models

Model artifacts aren't committed; generate them once:
```bash
python prediction/train_models.py
```
This creates `prediction/ml_models/diabetes_model.joblib` and
`heart_disease_model.joblib`. **These are trained on synthetic data for
scaffolding/demo purposes** — replace with models trained on real, properly
licensed clinical datasets before any non-prototype use.

### 7. Seed the chatbot knowledge base

```bash
python manage.py seed_symptoms
```

### 8. Run the server

```bash
python manage.py runserver
```

## API overview

All endpoints are under `/api/`. Authenticated endpoints expect
`Authorization: Bearer <access_token>`.

### Auth (`/api/accounts/`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `register/` | Create account (role: patient or doctor) |
| POST | `login/` | Returns `{user, tokens: {access, refresh}}` |
| POST | `token/refresh/` | Refresh access token |
| GET/PUT/PATCH | `profile/` | Current user's profile |
| POST | `change-password/` | Change password |

### Doctors (`/api/`)
| Method | Endpoint | Description |
|---|---|---|
| GET | `doctors/` | List/search doctors (filter by specialization, availability) |
| GET/PUT/PATCH/DELETE | `doctors/{id}/` | Doctor detail (owner/admin write) |
| CRUD | `specializations/` | Manage specializations |
| CRUD | `availability/` | Doctor's own weekly availability slots |

### Patients (`/api/`)
| Method | Endpoint | Description |
|---|---|---|
| CRUD | `patients/` | Patient profile (scoped: patients see only their own) |
| CRUD | `medical-records/` | Medical history (doctors create, patients view their own) |

### Appointments (`/api/`)
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `appointments/` | List (scoped by role) / book (patients) |
| GET/PUT/PATCH/DELETE | `appointments/{id}/` | Detail |
| PATCH | `appointments/{id}/set-status/` | Confirm / cancel / complete / no-show |

Booking an appointment automatically:
- Notifies both patient and doctor
- Schedules a `Reminder` 1 hour before the appointment

### Chatbot (`/api/chatbot/`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `chat/` | `{message, session_id?}` → bot reply with urgency + matched keywords |
| GET | `sessions/` | Past chat sessions for current user |
| CRUD | `symptoms/` | Manage the keyword → advice knowledge base |

### Prediction (`/api/prediction/`)
| Method | Endpoint | Body |
|---|---|---|
| POST | `diabetes/` | `{age, bmi, glucose, blood_pressure, family_history}` |
| POST | `heart-disease/` | `{age, cholesterol, resting_bp, max_heart_rate, smoker, diabetic}` |
| GET | `history/` | Past predictions for current user |

Each call returns `{risk_score (0-1), risk_label (Low/Moderate/High)}` and is
logged to `PredictionRecord`.

### Notifications (`/api/`)
| Method | Endpoint | Description |
|---|---|---|
| GET | `notifications/` | Current user's notifications |
| POST | `notifications/{id}/mark-read/` | Mark one as read |
| POST | `notifications/mark-all-read/` | Mark all as read |
| GET | `notifications/unread-count/` | Badge count |

### Reminders (`/api/`) — doctor/admin only
| Method | Endpoint | Description |
|---|---|---|
| CRUD | `reminders/` | Manage reminders |
| POST | `reminders/dispatch-due/` | Manually trigger sending of due reminders |

Run periodically via cron/Celery beat:
```bash
python manage.py dispatch_reminders
```

### Reports (`/api/reports/`) — doctor/admin only
| Method | Endpoint | Body |
|---|---|---|
| POST | `generate/` | `{report_type: patient_history\|doctor_performance\|appointment_summary, ...}` |
| GET | `reports/` | Previously generated reports |

### Dashboard (`/api/dashboard/`)
| Method | Endpoint | Role |
|---|---|---|
| GET | `admin/` | Admin — system-wide stats |
| GET | `doctor/` | Doctor — personal stats |
| GET | `patient/` | Patient — personal stats |

## Notes & next steps

- **UUID primary keys** are used throughout for security (non-sequential IDs).
- **Role enforcement** lives in `accounts/permissions.py` (`IsPatient`,
  `IsDoctor`, `IsAdminRole`, `IsOwnerOrAdmin`) and per-view custom permission
  classes — review and tighten for your actual access rules before production.
- **Chatbot** is intentionally rule-based (keyword matching) so it's
  transparent and easy to extend; swap `chatbot/engine.py`'s internals for an
  LLM/NLP call without touching views or serializers.
- **Prediction models** are demo logistic-regression models trained on
  synthetic data (`prediction/train_models.py`). Replace with real trained
  models before clinical use, and never treat this as a diagnostic tool.
- **Reminders dispatch** is a pull-based command (`dispatch_reminders`), not
  a background worker — wire it to cron or Celery beat in production.
- Add real email/SMS sending in `notifications/services.py` if you want
  notifications to leave the app (currently they're in-app only).
