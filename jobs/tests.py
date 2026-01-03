from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Application
from datetime import date


class ApplicationAPITest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="pass123")
        self.user2 = User.objects.create_user("user2", password="pass123")

    def authenticate(self, user):
        response = self.client.post("/api/token/", {
            "username": user.username,
            "password": "pass123"
        })
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_user_can_create_application(self):
        self.authenticate(self.user1)

        data = {
            "company_name": "Google",
            "position": "Backend Intern",
            "application_date": date.today(),
            "status": "APPLIED"
        }

        response = self.client.post("/api/applications/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_see_others_applications(self):
        Application.objects.create(
            user=self.user2,
            company_name="Meta",
            position="Engineer",
            application_date=date.today(),
            status="APPLIED"
        )

        self.authenticate(self.user1)
        response = self.client.get("/api/applications/")
        self.assertEqual(len(response.data), 0)
