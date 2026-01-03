from django.core.exceptions import ValidationError
import os

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]
MAX_FILE_SIZE_MB = 5


def validate_resume_file(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Only PDF and DOC/DOCX files are allowed.")

    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError("File size must be under 5MB.")
