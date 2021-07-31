"""ipavlov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from schedule import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserAdd.as_view()),
    path('users/<int:pk>/', views.UserEdit.as_view()),
    path('users/<int:pk>/inactivate/', views.UserInactivate.as_view()),
    path('timetable/doctor/<int:doctor_pk>/', views.TimetableList.as_view()),
    path('timetable/slot/<int:pk>/signup/', views.TimetableSignup.as_view()),
    path('timetable/slot/<int:pk>/cancel/', views.TimetableCancel.as_view()),
    path('timetable/stat/', views.TimetableStatistics.as_view()),
    path('api-token-auth/', obtain_auth_token)
]
