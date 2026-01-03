from django.urls import path
from .views import RegisterView,GoogleAuthView,MeView,LogoutView,ResumeDownloadView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

]
urlpatterns += [
    path(
        "applications/<int:application_id>/resume/",
        ResumeDownloadView.as_view(),
        name="download-resume"
    ),
]
