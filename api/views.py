from django.shortcuts import get_object_or_404
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
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import make_aware


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

    def perform_create(self, serializer):
        # Récupérer l'utilisateur connecté comme auteur de l'issue
        author_user = self.request.user
        project_id = self.kwargs.get("project_id")
        print(project_id)
        # Remplir automatiquement les champs requis de l'issue
        created_time = make_aware(datetime.now())  # Date et heure actuelles du serveur

        # Ajouter les valeurs aux données de l'issue
        issue_data = serializer.validated_data
        issue_data["created_time"] = created_time
        issue_data["author_user"] = author_user
        issue_data["project"] = project_id

        # Enregistrer l'issue dans la base de données
        serializer.save()


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

    def perform_create(self, serializer):
        # Récupérer l'utilisateur connecté comme auteur du commentaire
        author_user = self.request.user

        # Récupérer l'issue associée au commentaire en utilisant l'issue_id des paramètres d'URL
        issue_id = self.kwargs.get('issue_id')
        issue = get_object_or_404(Issues, pk=issue_id)

        # Remplir automatiquement les champs requis du commentaire
        created_time = timezone.now()

        # Ajouter les valeurs aux données du commentaire
        comment_data = serializer.validated_data
        comment_data["author_user"] = author_user
        comment_data["issue"] = issue
        comment_data["created_time"] = created_time

        # Enregistrer le commentaire dans la base de données
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AddUserToProjectView(APIView):
    def post(self, request, project_id):
        project = Projects.objects.get(id=project_id)

        # Vérifier si l'utilisateur est l'auteur du projet
        if project.author_user != request.user:
            return Response(
                {
                    "message": "Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        contributor_data = (
            request.data.copy()
        )  # Créer une copie mutable de la QueryDict
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
        return Response(
            {"message": "Utilisateur supprimé du projet avec succès."},
            status=status.HTTP_204_NO_CONTENT,
        )


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
    def post(self, request, project_id, issue):
        project = Projects.objects.get(id=project_id)
        comment_data = {
            "description": request.data.get("description"),
            "author_user": request.user.id,
            "issue": issue,  # Utilisez directement issue_id
        }
        serializer = CommentSerializer(
            data=comment_data, context=self.get_serializer_context()
        )
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
