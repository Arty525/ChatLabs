from django.contrib import admin

from users.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'telegram_id')
    search_fields = ('email', 'first_name', 'last_name', 'telegram_id')
    ordering = ('email', 'first_name', 'last_name')