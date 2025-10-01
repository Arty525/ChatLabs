from datetime import datetime
import os
import re
import django
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from django.conf import settings
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from bot.utils import get_welcome_message, add_tg_id, get_user_tasks
from aiogram.filters.state import State, StatesGroup


class Form(StatesGroup):
    waiting_for_email = State()


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
            BotCommand(command="start", description="🤖Запустить бота"),
            BotCommand(command="menu", description="📱Показать главное меню"),
        ]
        await self.bot.set_my_commands(commands)

    def setup_handlers(self):
        @self.dp.message(Command("menu"))
        async def cmd_menu(message: types.Message):
            await message.answer("📱Главное меню", reply_markup=self.get_main_menu())

        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message, state: FSMContext):
            """Обработчик команды /start"""
            user = message.from_user
            welcome_text, is_registered = await get_welcome_message(user.id)
            if is_registered:
                await message.answer(welcome_text, reply_markup=self.get_main_menu())
                await state.clear()
            else:
                await message.answer(welcome_text)
                await state.set_state(Form.waiting_for_email)

        @self.dp.message(Form.waiting_for_email, F.text.regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'))
        async def registration(message: types.Message, state: FSMContext):
            user = message.from_user
            message_text, is_registered = await add_tg_id(message.text, user.id)
            await message.answer(message_text)
            if is_registered:
                await state.clear()

        @self.dp.message(Form.waiting_for_email)
        async def bad_email_input(message: types.Message, state: FSMContext):
            await message.answer("❌Please enter a valid email address.")

        @self.dp.callback_query(F.data == "my_tasks")
        async def cmd_profile(callback: types.CallbackQuery):
            tasks = await get_user_tasks(callback.from_user.id)
            await callback.message.answer('📃Список задач')
            for task in tasks:
                message_text = f'''Task: {task['title']}
Category: {task['category']}
Created at: {datetime.fromisoformat(task['created_at']).strftime("%d.%m.%Y %H:%M")}
Deadline: {datetime.fromisoformat(task['deadline']).strftime("%d.%m.%Y %H:%M")}
Description: {task['description']}
Status: {task['status']}'''
                await callback.message.answer(message_text)
            await callback.answer()


    async def start_polling(self):
        """Запуск бота в режиме polling"""
        print("🤖 Telegram бот запущен")
        await self.set_bot_commands()
        await self.dp.start_polling(self.bot)
