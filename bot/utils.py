from asgiref.sync import sync_to_async
from users.models import User


async def get_welcome_message(tg_id):
    is_registered = False
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=tg_id)
        message = 'Hello! You are already registered.'
        is_registered = True
    except User.DoesNotExist:
        message = 'Hello! To register your Telegram ID, enter your registered Email'
    except Exception as e:
        message = f'Sorry, an error occurred: {str(e)}'
    finally:
        return message, is_registered

async def add_tg_id(email, tg_id):
    try:
        user = await sync_to_async(User.objects.get)(email=email)
        user.telegram_id = tg_id
        await sync_to_async(user.save)()
        message = 'Telegram ID added successfully'
    except User.DoesNotExist:
        message = 'User with the provided Email was not found'
    except Exception as e:
        message = f'Sorry, an error occurred: {str(e)}'
    return message

