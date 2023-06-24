from rest_framework import viewsets, permissions
from rest_framework.views import APIView
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
from .permissions import IsProjectContributor, IsIssueAuthor, IsCommentAuthor
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer
from rest_framework.viewsets import ModelViewSet


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
    permission_classes = [IsProjectContributor]

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)
        Contributors.objects.create(
            project=project, user=self.request.user, role="Author"
        )

    def get_queryset(self):
        if self.action == "list":
            # Filtrer le queryset pour les contributeurs
            return self.request.user.contributed_projects.all()
        else:
            return Projects.objects.all()


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


class AddUserToProjectView(APIView):
    def post(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributor_data = request.data
        contributor_data["project"] = project.id
        serializer = ContributorSerializer(data=contributor_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersInProjectView(APIView):
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        contributors = Contributors.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)


class RemoveUserFromProjectView(APIView):
    def delete(self, request, project_id, user_id):
        project = Projects.objects.get(id=project_id)
        contributor = Contributors.objects.get(project=project, user=user_id)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssuesInProjectView(APIView):
    def get(self, request, project_id):
        project = Projects.objects.get(id=project_id)
        issues = Issues.objects.filter(project=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)


class UpdateIssueInProjectView(APIView):
    def put(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteIssueFromProjectView(APIView):
    def delete(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCommentInIssueView(APIView):
    def post(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        comment_data = request.data
        comment_data["issue"] = issue.id
        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsInIssueView(APIView):
    def get(self, request, project_id, issue_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        comments = Comments.objects.filter(issue=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class UpdateCommentView(APIView):
    def put(self, request, project_id, issue_id, comment_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        comment = Comments.objects.get(id=comment_id, issue=issue)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(APIView):
    def delete(self, request, project_id, issue_id, comment_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        comment = Comments.objects.get(id=comment_id, issue=issue)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentDetailView(APIView):
    def get(self, request, project_id, issue_id, comment_id):
        project = Projects.objects.get(id=project_id)
        issue = Issues.objects.get(id=issue_id, project=project)
        comment = Comments.objects.get(id=comment_id, issue=issue)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
