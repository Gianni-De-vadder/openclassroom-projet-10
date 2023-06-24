from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


# This is a custom permission class in Python that checks if the user making the request is a
# contributor to a specific project object.
class IsProjectContributor(BasePermission):
    message = "You have to be a contributor of this project, or the creator."

    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur est le créateur du projet
        if obj.author_user == request.user:
            return True

        # Vérifier si l'utilisateur est un contributeur du projet
        return obj.contributors.filter(pk=request.user.pk).exists()


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
