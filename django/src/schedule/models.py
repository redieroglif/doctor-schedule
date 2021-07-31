from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
import datetime
from django.utils import timezone
import pytz
from .tasks import generate_timetable_async
from celery.result import AsyncResult
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

tz = pytz.timezone(settings.TIME_ZONE)

class User(AbstractUser):
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    first_name = models.CharField('Имя', max_length=50, blank=True)
    patronymic_name = models.CharField('Отчество', max_length=50, blank=True)
    SEX_CHOISES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
    ]
    sex = models.CharField('Пол', max_length=50, null=True, blank= True, choices=SEX_CHOISES)
    birthdate = models.DateField('Дата рождения', blank=True, null=True)
    
    # FOR DOCTORS
    days_count = models.IntegerField('Количество дней для генерации расписания (для врачей)', help_text='Количество дней, на которое генерируются слоты для записи на приём (по умолчанию, на 7 дней вперёд)', default=7)
    appointment_time = models.DurationField('Длительность приема (для врачей)', default=datetime.timedelta(minutes=20))

    def fullname(self):
        if self.last_name or self.first_name or self.patronymic_name:
            return f'{self.last_name} {self.first_name} {self.patronymic_name}'
        else:
            return ''
    fullname.short_description = 'ФИО'

    def __str__(self):
        return f'{self.fullname()} ({self.username})' if self.fullname() else self.username

    def get_working_hours(self, days = range(7)):
        return self.timerange_set.filter(break_time = False, day__in = days)
    
    def get_break_hours(self, days = range(7)):
        return self.timerange_set.filter(break_time = True, day__in = days)

    def get_future_vacations(self):
        return self.vacation_set.filter(start__gte = timezone.now())
    
    def is_a_doctor(self):
        doc_group = Group.objects.get_or_create(name='Doctors')[0]
        return doc_group in self.groups.all()

    def generate_timetable(self, start_date, ignore_doctor_check = False):
        if self.is_a_doctor() or ignore_doctor_check:
            for i in range(self.days_count):
                day = start_date + datetime.timedelta(days=i)
                vacations = self.get_future_vacations().filter(start__date__lte = day, end__date__gte = day)
                if not vacations:
                    weekday = day.weekday()
                    timeranges = self.get_working_hours(days = [weekday])
                    for timerange in timeranges:
                        slot_begin = datetime.datetime.combine(day, timerange.start)
                        slot_end = slot_begin + self.appointment_time
                        day_end = datetime.datetime.combine(day, timerange.end)
                        while slot_end <= day_end:
                            breaks = self.get_break_hours(days=[weekday]).filter(start__gte = slot_begin, start__lt = slot_end)
                            existing = Timetable.objects.filter(
                                    Q(doctor=self),
                                    Q(start__gt = slot_begin, start__lt = slot_end) |
                                    Q(end__gt = slot_begin, start__lt = slot_end) |
                                    Q(start__lte=slot_begin, end__gte=slot_end)
                                )
                            if existing:
                                existing_end = existing.order_by("-end").first().end
                                slot_begin = timezone.make_naive(existing_end)
                            elif breaks:
                                breaks_end = breaks.order_by("-end").first().end
                                slot_begin = datetime.datetime.combine(day, breaks_end)
                            else:
                                timetable = Timetable(
                                    doctor = self,
                                    start = timezone.make_aware(slot_begin),
                                    end = timezone.make_aware(slot_end)
                                )
                                timetable.save()
                                slot_begin = slot_end

                            slot_end = slot_begin + self.appointment_time

def groups_changed(sender, instance, action, pk_set, **kwargs):
    try:
        doc_group = Group.objects.get(name='Doctors')
    except:
        return None
    if pk_set and doc_group.id in pk_set and action == "post_add":
        instance.generate_timetable(timezone.now(), ignore_doctor_check = True)
    elif (pk_set and doc_group.id in pk_set and action == "post_remove") or action == "post_clear":
        Timetable.objects.filter(doctor=instance).delete()

m2m_changed.connect(groups_changed, sender=User.groups.through)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class TimeRange(models.Model):
    doctor = models.ForeignKey('User', on_delete=models.CASCADE)
    DAYS_CHOISES = list(enumerate(["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]))
    day = models.IntegerField('День недели', choices=DAYS_CHOISES)
    start = models.TimeField('Начало диапазона')
    end = models.TimeField('Конец диапазона')
    break_time = models.BooleanField('Перерыв?', default=False)
    
class Vacation(models.Model):
    doctor = models.ForeignKey('User', on_delete=models.CASCADE)
    start = models.DateTimeField('Начало отпуска')
    end = models.DateTimeField('Конец отпуска')

class Timetable(models.Model):
    doctor = models.ForeignKey('User', on_delete=models.CASCADE, related_name='doctors_timetables')
    client = models.ForeignKey('User', on_delete=models.SET_NULL, null = True, related_name='users_timetables')
    start = models.DateTimeField('Начало приема')
    end = models.DateTimeField('Конец приема')
    
    def __str__(self):
        string = f'{self.doctor} @ {self.start.astimezone(tz=tz).strftime("%a %d.%m.%Y, %H:%M")} - {self.end.astimezone(tz=tz).strftime("%H:%M")}'
        if self.client:
            string += f' ({self.client})'
        return string