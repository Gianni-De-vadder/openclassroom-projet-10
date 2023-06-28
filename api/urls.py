from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
    SignupView,
    LoginView,
    AddUserToProjectView,
    RemoveUserFromProjectView,
    CreateCommentInIssueView,
)

# Création du routeur principal
router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")

# URLs pour les projets
urlpatterns = [
    # URLs pour l'authentification JWT
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # URLs pour les projets
    path("", include(router.urls)),
]

# URLs pour les problèmes liés à un projet
urlpatterns += [
    path(
        "projects/<int:project_id>/issues/",
        IssueViewSet.as_view({"get": "list", "post": "create"}),
        name="project-issues",
    ),
    path(
        "projects/<int:project_id>/issues/<int:pk>/",
        IssueViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="project-issue-detail",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/",
        CreateCommentInIssueView.as_view(),
        name="create_comment_in_issue",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="issue-comment-detail",
    ),
    path(
        "projects/<int:project_id>/users/",
        AddUserToProjectView.as_view(),
        name="add_user_to_project",
    ),
    path(
        "projects/<int:project_id>/users/<int:user_id>/",
        RemoveUserFromProjectView.as_view(),
        name="remove_user_from_project",
    ),
]

# Ajoutez d'autres URLs si nécessaire
