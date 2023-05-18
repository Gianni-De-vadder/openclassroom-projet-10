from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS


# This is a custom permission class in Python that checks if the user making the request is a
# contributor to a specific project object.
class IsProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(user_id=request.user.id).exists()


# The class `IsContributorOrReadOnly` checks if the request method is safe or not and returns True or
# False accordingly.
class IsContributorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False


# This class checks if the requesting user is the author of the object being accessed.
class IsIssueAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


# This class checks if the requesting user is the author of a comment object.
class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
