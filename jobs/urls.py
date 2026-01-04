from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    GoogleAuthView,
    MeView,
    LogoutView,
    ResumeDownloadView,
    ApplicationViewSet,
    ApplicationsSummaryView,InterviewListCreateView,
    CoverLetterDownloadView
)

router = DefaultRouter()
router.register(
    r"applications",
    ApplicationViewSet,
    basename="application"
)

urlpatterns = [
    # AUTH
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

    # CUSTOM ENDPOINT
    path(
        "applications/<int:application_id>/resume/",
        ResumeDownloadView.as_view(),
        name="download-resume"
    ),
    path(
        "applications/<int:application_id>/cover-letter/",
        CoverLetterDownloadView.as_view(),
        name="download-cover-letter",
    ),
    path("applications/summary/", ApplicationsSummaryView.as_view(), name="applications-summary"),
     path(
        "applications/<int:application_id>/interviews/",
        InterviewListCreateView.as_view(),
        name="application-interviews"
    ),
]

# 🔥 THIS IS THE IMPORTANT PART
urlpatterns += router.urls
