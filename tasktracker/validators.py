from django.utils import timezone
from rest_framework.serializers import ValidationError


class TaskDeadlineValidator:
    """Checks if the deadline is not earlier than the current date"""

    def __init__(self, deadline):
        self.deadline = deadline

    def __call__(self, fields):
        if fields.get("deadline"):
            if fields.get("deadline") < timezone.now():
                raise ValidationError("Deadline cannot be earlier than now")
