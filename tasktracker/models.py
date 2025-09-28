import ulid
from django.db import models


# Create your models here.
def generate_ulid():
    return str(ulid.new())

class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=26, default=generate_ulid)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id} {self.title}'


    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Task(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired')
    )
    id = models.CharField(primary_key=True, max_length=26, default=generate_ulid)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.id} {self.title} | status: {self.status}, owner: {self.owner}, category: {self.category}, '
                f'deadline: {self.deadline}')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
