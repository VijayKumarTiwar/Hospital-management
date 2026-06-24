import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from doctors.models import Doctor, Specialization
from patients.models import Patient
from appointments.models import Appointment

print("Clearing old data...")
Appointment.objects.all().delete()
Patient.objects.all().delete()
Doctor.objects.all().delete()
Specialization.objects.all().delete()
# keep superusers, delete others
User.objects.exclude(is_superuser=True).delete()

print("Creating Admin User...")
if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser(username="admin", email="admin@example.com", password="password")

print("Creating specializations...")
cardio = Specialization.objects.create(name="Cardiology", description="Heart related issues")
neuro = Specialization.objects.create(name="Neurology", description="Brain and nervous system")
pedia = Specialization.objects.create(name="Pediatrics", description="Child healthcare")

print("Creating Doctors...")
def create_doctor(username, first_name, last_name, spec, license_num):
    u = User.objects.create_user(username=username, email=f"{username}@hospital.com", password="password", role=User.Role.DOCTOR, first_name=first_name, last_name=last_name)
    d = Doctor.objects.create(user=u, license_number=license_num, years_of_experience=10, consultation_fee=500.00)
    d.specializations.add(spec)
    return d

d1 = create_doctor("drsmith", "John", "Smith", cardio, "LIC-1001")
d2 = create_doctor("drjane", "Jane", "Doe", neuro, "LIC-1002")
d3 = create_doctor("drbob", "Bob", "Wilson", pedia, "LIC-1003")

print("Creating Patients...")
def create_patient(username, first_name, last_name):
    u = User.objects.create_user(username=username, email=f"{username}@mail.com", password="password", role=User.Role.PATIENT, first_name=first_name, last_name=last_name)
    p = Patient.objects.create(user=u, blood_group=Patient.BloodGroup.O_POS, gender=Patient.Gender.MALE)
    return p

p1 = create_patient("patient1", "Alice", "Brown")
p2 = create_patient("patient2", "Charlie", "Davis")
p3 = create_patient("patient3", "Eve", "Evans")

print("Creating Appointments...")
now = timezone.now()
Appointment.objects.create(patient=p1, doctor=d1, scheduled_at=now + timedelta(days=1), status=Appointment.Status.CONFIRMED, reason="Heart checkup")
Appointment.objects.create(patient=p2, doctor=d2, scheduled_at=now + timedelta(days=2), status=Appointment.Status.PENDING, reason="Headache")
Appointment.objects.create(patient=p3, doctor=d3, scheduled_at=now + timedelta(days=3), status=Appointment.Status.CONFIRMED, reason="Fever")
Appointment.objects.create(patient=p1, doctor=d2, scheduled_at=now - timedelta(days=1), status=Appointment.Status.COMPLETED, reason="General checkup")

print("Dummy data added successfully!")
