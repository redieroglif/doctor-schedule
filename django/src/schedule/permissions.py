
from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsInGroup(permissions.BasePermission):
    required_groups = []

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return has_group_permission

class IsManager(IsInGroup):
    required_groups = ['Managers']

class IsClient(IsInGroup):
    required_groups = ['Clients']

class IsDoctor(IsInGroup):
    required_groups = ['Doctor']