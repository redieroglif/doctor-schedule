from celery import shared_task
from django.utils import timezone
# from datetime import timedelta
import schedule.models
from django.contrib.auth.models import Group

@shared_task
def generate_timetable_async(user_id):
    doctor = schedule.models.User.objects.get(id = user_id)
    now = timezone.now()
    doctor.generate_timetable(now)

@shared_task
def generate_all_timetables():
    doc_group = Group.objects.get_or_create(name="Doctors")[0]
    doctors = schedule.models.User.objects.filter(groups = doc_group)
    for doctor in doctors:
        generate_timetable_async.delay(doctor.id)