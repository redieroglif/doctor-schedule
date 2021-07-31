from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TimeRange, Vacation, Timetable
from rest_framework.authtoken.admin import TokenAdmin
    
class TimeInline(admin.TabularInline):
    model = TimeRange
    extra = 14

class VacationInline(admin.TabularInline):
    model = Vacation
    extra = 3

@admin.register(User)
class CustomUserAdmin(UserAdmin):    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('last_name', 'first_name', 'patronymic_name', 'sex', 'email')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Параметры врача', {'fields': ('appointment_time','days_count')})
    )
    list_display = ('username', 'fullname', 'email', 'is_staff', 'is_active')
    inlines = (TimeInline,VacationInline)
    
admin.site.register(Timetable, admin.ModelAdmin)