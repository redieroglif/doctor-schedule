from .models import User, Timetable
from django.contrib.auth.models import Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name', 'patronymic_name', 'sex', 'birthdate','groups']

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'start', 'end']
    