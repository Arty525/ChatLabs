from django.contrib import admin

from tasktracker.models import Task, Category


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "status",
        "created_at",
        "updated_at",
        "deadline",
        "category",
        "owner",
    )
    list_filter = ("status", "owner", "category")
    search_fields = ("title", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
