from .models import User, Timetable
from django.contrib.auth.models import Group
from rest_framework import permissions, status
from rest_framework.views import APIView
from .serializers import UserSerializer, TimetableSerializer
from .permissions import IsManager, IsClient
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from django.utils import timezone
import datetime
from django.http import Http404

class UserAdd(mixins.CreateModelMixin,
              generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserEdit(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class UserInactivate(APIView):
    permission_classes = [IsManager]

    def get_user(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        user = self.get_user(pk)
        user.is_active = False
        user.groups.clear()
        user.save()
        return Response(status=status.HTTP_200_OK)

class TimetableList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_doctor(self, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        finally:
            if user.is_a_doctor():
                return User.objects.get(pk=pk)
            else:
                raise Http404
            
    def get(self, request, doctor_pk, format=None):
        queryset = Timetable.objects.filter(
                        doctor = self.get_doctor(doctor_pk),
                        start__gt = timezone.now(),
                        client__isnull = True
                    ).order_by('start')
        serializer = TimetableSerializer(queryset, many=True)
        return Response(serializer.data)

class TimetableSignup(APIView):
    permission_classes = [IsClient]

    def get_timetable(self, pk):
        try:
            return Timetable.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def patch(self, request, pk, format=None):
        slot = self.get_timetable(pk)
        if slot.client != None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            slot.client = request.user
            slot.save()
            return Response(status=status.HTTP_200_OK)

class TimetableCancel(APIView):
    permission_classes = [IsClient]

    def get_timetable(self, pk):
        try:
            return Timetable.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def patch(self, request, pk, format=None):
        slot = self.get_timetable(pk)
        if slot.client != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            slot.client = None
            slot.save()
            return Response(status=status.HTTP_200_OK)
    
class TimetableStatistics(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_start(self, request):
        if request.GET.get('start_date'):
            return datetime.datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
        else:
            return timezone.now().date()
    
    def get_end(self, request, start_date):
        if request.GET.get('end_date'):
            return datetime.datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
        else:
            return start_date + datetime.timedelta(days=30)

    def get(self, request, format=None):
        start_date = self.get_start(request)
        end_date = self.get_end(request, start_date)
        days = (end_date - start_date).days + 1
        data = [{"start":start_date,"end":end_date}]

        for d in range(days):
            day = start_date + datetime.timedelta(days=d)
            count = Timetable.objects.filter(
                        start__date = day, 
                        client__isnull = False
                    ).count()
            if count > 0:
                day_data = {"day":day, "count":count}
                data.append(day_data)

        return Response(data)
