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
)


# Création du routeur
from rest_framework_nested import routers

# Création du routeur principal
router = routers.DefaultRouter()

# Enregistrement de la vue pour la gestion des projets
router.register(r"projects", ProjectViewSet, basename="projects")

# Création du routeur pour les problèmes liés à un projet
project_router = routers.NestedDefaultRouter(router, r"projects", lookup="project")
project_router.register(r"issues", IssueViewSet, basename="issues")

# Création du routeur pour les commentaires liés à un problème
issue_router = routers.NestedDefaultRouter(project_router, r"issues", lookup="issue")
issue_router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    # URLs pour l'authentification JWT
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # URLs pour les projets
    path("", include(router.urls)),
    # URLs pour les problèmes liés à un projet
    path("", include(project_router.urls)),
    # URLs pour les commentaires liés à un problème
    path("", include(issue_router.urls)),
]
