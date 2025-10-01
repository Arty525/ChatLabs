import os
import re

import django
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from django.conf import settings
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from bot.utils import get_welcome_message, add_tg_id


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.setup_handlers()

    def get_main_menu(self):
        """Главное меню бота"""

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Мои задачи", callback_data="my_tasks")],
                [InlineKeyboardButton(text="➕ Создать задачу", callback_data="create_task")],
                [InlineKeyboardButton(text="📊 Категории", callback_data="stats")],
            ]
        )

        return keyboard

    async def set_bot_commands(self):
        """Установка команд меню бота"""
        commands = [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="menu", description="Показать главное меню"),
        ]
        await self.bot.set_my_commands(commands)

    def setup_handlers(self):
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            """Обработчик команды /start"""
            user = message.from_user
            print(user.id)
            welcome_text, is_registered = await get_welcome_message(user.id)
            if is_registered:
                await message.answer(welcome_text, reply_markup=self.get_main_menu())
            else:
                await message.answer(welcome_text)
            @self.dp.message(lambda message: re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message.text))
            async def registration(message: types.Message):
                message_text = await add_tg_id(message.text, user.id)
                await message.answer(message_text)

            @self.dp.message()
            async def bad_input(message: types.Message):
                message_text = 'Email input is not valid. Please try again.'
                await message.answer(message_text)




        @self.dp.callback_query(F.data == "my_tasks")
        async def cmd_profile(callback: types.CallbackQuery):
            await callback.answer()
            await callback.message.answer('Список задач')



    async def start_polling(self):
        """Запуск бота в режиме polling"""
        print("🤖 Telegram бот запущен")
        await self.set_bot_commands()
        await self.dp.start_polling(self.bot)
