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
router = DefaultRouter()

# Enregistrement des routes pour les vues API
router.register(r"contributors", ContributorViewSet, basename="contributor")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")

# Ajout des routes du routeur aux routes globales de l'application
urlpatterns = [
    # URLs pour l'authentification JWT
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Ajout des routes du routeur aux routes globales de l'application
urlpatterns += router.urls
