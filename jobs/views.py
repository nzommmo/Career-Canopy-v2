from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import FileResponse, Http404
from .models import Application



class ApplicationViewSet(ModelViewSet):
    """
    Core security logic lives here.
    """

    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        CRITICAL SECURITY METHOD.

        Ensures users only see THEIR OWN applications.
        """
        return Application.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user.
        Prevents user spoofing.
        """
        serializer.save(user=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            name = idinfo.get("name", "")

            # 🔑 LINKING LOGIC (THIS IS THE KEY PART)
            user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name
                )
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "auth_provider": "google"
            })

        except ValueError:
            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        


class MeView(APIView):
    """
    Returns the currently authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)



class LogoutView(APIView):
    """
    Logout by blacklisting the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResumeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            application = Application.objects.get(
                id=application_id,
                user=request.user  # 🔐 OWNER CHECK
            )

            if not application.resume:
                raise Http404("No resume uploaded")

            return FileResponse(
                application.resume.open(),
                as_attachment=True,
                filename=application.resume.name.split("/")[-1]
            )

        except Application.DoesNotExist:
            raise Http404("Resume not found")
