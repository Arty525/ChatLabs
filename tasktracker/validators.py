from rest_framework.serializers import ValidationError


class TaskDeadlineValidator:
    '''Checks if the deadline is not earlier than the current date'''
    def __init__(self, deadline, created_at):
        self.deadline = deadline
        self.created_at = created_at

    def __call__(self, fields):
        if fields.get('deadline') and fields.get('created_at'):
            if fields.get('deadline') < fields.get('created_at'):
                raise ValidationError('Deadline cannot be earlier than created at')
