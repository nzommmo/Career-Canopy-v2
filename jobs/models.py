from django.db import models
from django.contrib.auth.models import User
from .validators import validate_resume_file



def resume_upload_path(instance, filename):
    """
    Store resumes per user to avoid collisions and leaks.
    Example: resumes/user_3/mycv.pdf
    """
    return f"resumes/user_{instance.user.id}/{filename}"


def cover_letter_upload_path(instance, filename):
    return f"cover_letters/user_{instance.user.id}/{filename}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("APPLIED", "Applied"),
        ("INTERVIEWING", "Interviewing"),
        ("OFFER", "Offer"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    resume = models.FileField(
        upload_to=resume_upload_path,
        validators=[validate_resume_file],
        null=True,
        blank=True
    )

    cover_letter = models.FileField(
        upload_to=cover_letter_upload_path,
        validators=[validate_resume_file],
        null=True,
        blank=True
    )
    application_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="APPLIED"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.position}"

class Interview(models.Model):
    """
    Child model of Application.
    One application can have multiple interviews.
    """

    INTERVIEW_TYPE_CHOICES = [
        ("PHONE", "Phone Screen"),
        ("TECHNICAL", "Technical"),
        ("BEHAVIORAL", "Behavioral"),
        ("SYSTEM_DESIGN", "System Design"),
        ("ONSITE", "On-site"),
        ("FINAL", "Final"),
        ("HR", "HR"),
        ("OTHER", "Other"),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    interview_date = models.DateTimeField()
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)

    def __str__(self):
        return f"{self.interview_type} - {self.application.company_name}"



