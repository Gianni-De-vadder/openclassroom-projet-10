from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ContributorSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .models import Contributors, Projects, Comments, Issues
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class ContributorViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class IssueViewSet(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
