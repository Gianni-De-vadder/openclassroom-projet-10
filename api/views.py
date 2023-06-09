from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    ContributorSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .models import Contributors, Projects, Comments, Issues
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets, permissions
from .permissions import IsProjectContributor, IsIssueAuthor, IsCommentAuthor
from api.permissions import IsContributorOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh_token = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Inscription réussie"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewSet(ModelViewSet):
    """
    ViewSet for contributors.
    Allows creating, retrieving, updating, and deleting contributors.
    """

    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(ModelViewSet):
    """
    ViewSet for projects.
    Allows creating, retrieving, updating, and deleting projects.
    Unauthorized users can only perform read operations.
    Only the author of a project or a contributor can modify or delete it.
    """

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsContributorOrReadOnly]

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsProjectContributor]
        return super().get_permissions()



class IssueViewSet(ModelViewSet):
    """
    ViewSet for issues.
    Allows creating, retrieving, updating, and deleting issues.
    Unauthorized users can only perform read operations.
    Only authors of issues have the right to modify or delete their own issues.
    """

    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueAuthor]


class CommentViewSet(ModelViewSet):
    """
    ViewSet for comments.
    Allows creating, retrieving, updating, and deleting comments.
    Unauthorized users can only perform read operations.
    Only authors of comments have the right to modify or delete their own comments.
    """

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]
