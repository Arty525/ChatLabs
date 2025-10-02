from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import requests
from tasktracker.models import Task
from django.conf import settings


@shared_task
def update_task_status():
    now = timezone.now()
    expired_tasks = Task.objects.filter(
        deadline__lt=now, status__in=["created", "in_progress"]
    )
    updated_count = 0
    for task in expired_tasks:
        task.status = "expired"
        task.save()
        updated_count += 1
    return f"Updated {updated_count} tasks"


@shared_task
def send_reminder():
    now = timezone.now()
    reminder_time = now + timedelta(hours=24)
    tasks_to_remind = Task.objects.filter(
        deadline__range=(now, reminder_time),
        status__in=["created", "in_progress"],
        owner__telegram_id__isnull=False,
    ).select_related("owner")
    sent_count = 0
    for task in tasks_to_remind:
        try:
            if send_telegram_reminder(task.owner.telegram_id, task):
                sent_count += 1
        except Exception:
            continue
    return f"Sent {sent_count} reminders"


def send_telegram_reminder(telegram_id, task):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    local_timezone = timezone.get_current_timezone()
    local_deadline = timezone.localtime(task.deadline, local_timezone)
    deadline_str = local_deadline.strftime("%d.%m.%Y at %H:%M") if task.deadline else "not set"
    message_text = (
        f"🔔 **TASK REMINDER**\n\n"
        f"💼 *Task:* {task.title}\n"
        f"📅 *Deadline:* {deadline_str}\n"
        f"📝 *Description:* {task.description[:100]}{'...' if len(task.description) > 100 else ''}\n"
        f"🏷️ *Status:* {task.get_status_display()}\n"
        f"🆔 *Task ID:* {task.id}\n\n"
        f"⏰ Time to complete the task is running out!"
    )
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": telegram_id, "text": message_text, "parse_mode": "Markdown"}
    response = requests.post(url, json=data, timeout=10)
    if response.status_code == 200:
        return True
    else:
        return False
