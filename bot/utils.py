from datetime import datetime
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from asgiref.sync import sync_to_async
from users.models import User
import requests
import aiohttp


async def get_welcome_message(tg_id):
    is_registered = False
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=tg_id)
        message = 'Hello! You are already registered.'
        is_registered = True
    except User.DoesNotExist:
        message = 'Hello! To register your Telegram ID, enter your registered Email'
    except Exception as e:
        message = f'⚠️ Sorry, an error occurred: {str(e)}'
    finally:
        return message, is_registered

async def add_tg_id(email, tg_id):
    is_registered = False
    try:
        user = await sync_to_async(User.objects.get)(email=email)
        user.telegram_id = tg_id
        await sync_to_async(user.save)()
        message = '✅ Telegram ID added successfully'
        is_registered = True
    except User.DoesNotExist:
        message = '❌ User with the provided Email was not found'
    except Exception as e:
        message = f'⚠️ Sorry, an error occurred: {str(e)}'
    return message, is_registered

async def get_user_tasks(tg_id, category=None):
    params = {'telegram_id': tg_id, 'category': category}
    response = requests.get(f'http://127.0.0.1:8000/api/tasks_list/', params=params)
    result = response.json()
    messages = []
    for task in result:
        message_text = f'''💼 Task: {task['title']}
        🗂️ Category: {task['category']}
        🕒 Created at: {datetime.fromisoformat(task['created_at']).strftime("%d.%m.%Y %H:%M")}
        🕒 Deadline: {datetime.fromisoformat(task['deadline']).strftime("%d.%m.%Y %H:%M")}
        📃 Description: {task['description']}
        🏷️ Status: {task['status']}'''
        messages.append(message_text)
    if len(messages) == 0:
        return '❌ No tasks found'
    return messages

async def get_categories(prefix=None):
    response = requests.get('http://127.0.0.1:8000/api/category/')
    result = response.json()
    keyboard_buttons = []
    for category in result:
        keyboard_buttons.append([InlineKeyboardButton(text=f'{prefix or ''}{category['title']}', callback_data=f"{prefix or ''}category_{category['title']}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def save_task(task_data, tg_id):
    try:
        response = requests.post(
            f'http://127.0.0.1:8000/api/new_task/?telegram_id={tg_id}',
            json=task_data,
            timeout=10  # ✅ Таймаут 10 секунд
        )

        if response.status_code == 201:
            return '✅ Task added successfully', True
        elif response.status_code == 400:
            result = response.json()
            if result.get('non_field_errors'):
                return '❌ Deadline cannot be earlier than now', False
            else:
                return f'❌ Validation error: {result}', False
        else:
            return f'❌ Server error: {response.status_code}', False

    except requests.exceptions.Timeout:
        return '❌ Request timeout - server not responding', False
    except requests.exceptions.ConnectionError:
        return '❌ Connection error - check server', False
    except Exception as e:
        return f'❌ An error occurred: {str(e)}', False
