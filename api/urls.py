from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ContributorViewSet,
    ProjectViewSet,
    IssueViewSet,
    CommentViewSet,
    SignupView,
    LoginView,
    AddUserToProjectView,
    UsersInProjectView,
    RemoveUserFromProjectView,
    IssuesInProjectView,
    UpdateIssueInProjectView,
    DeleteIssueFromProjectView,
    CreateCommentInIssueView,
    CommentsInIssueView,
    UpdateCommentView,
    DeleteCommentView,
    CommentDetailView,
)


# Création du routeur
router = DefaultRouter()

# Enregistrement des routes pour les vues API
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"projects", ProjectViewSet, basename="project-delete")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")

# Ajout des routes du routeur aux routes globales de l'application
urlpatterns = [
    # URLs pour l'authentification JWT
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "projects/<int:id>/users/",
        AddUserToProjectView.as_view(),
        name="add_user_to_project",
    ),
    path(
        "projects/<int:id>/users/",
        UsersInProjectView.as_view(),
        name="users_in_project",
    ),
    path(
        "projects/<int:id>/users/<int:user_id>/",
        RemoveUserFromProjectView.as_view(),
        name="remove_user_from_project",
    ),
    path(
        "projects/<int:id>/issues/",
        IssuesInProjectView.as_view(),
        name="issues_in_project",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/",
        UpdateIssueInProjectView.as_view(),
        name="update_issue_in_project",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/",
        DeleteIssueFromProjectView.as_view(),
        name="delete_issue_from_project",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/comments/",
        CreateCommentInIssueView.as_view(),
        name="create_comment_in_issue",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/comments/",
        CommentsInIssueView.as_view(),
        name="comments_in_issue",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/comments/<int:comment_id>/",
        UpdateCommentView.as_view(),
        name="update_comment",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/comments/<int:comment_id>/",
        DeleteCommentView.as_view(),
        name="delete_comment",
    ),
    path(
        "projects/<int:id>/issues/<int:issue_id>/comments/<int:comment_id>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
]

# Ajout des routes du routeur aux routes globales de l'application
urlpatterns += router.urls
