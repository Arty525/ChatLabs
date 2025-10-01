import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from unicodedata import category

from bot.utils import get_welcome_message, add_tg_id, get_user_tasks, get_categories, save_task
from aiogram.filters.state import State, StatesGroup


class Form(StatesGroup):
    waiting_for_email = State()
    waiting_for_task_title = State()
    waiting_for_task_category = State()
    waiting_for_task_deadline = State()
    waiting_for_task_description = State()


class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.session = None
        self.setup_handlers()

    def get_main_menu(self):
        """Bot main menu"""
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 My tasks", callback_data="my_tasks")],
                [InlineKeyboardButton(text="➕ Create task", callback_data="create_task")],
                [InlineKeyboardButton(text="🗂️ Categories", callback_data="categories")],
            ]
        )
        return keyboard

    async def set_bot_commands(self):
        """Setting bot commands"""
        commands = [
            BotCommand(command="start", description="🤖 Start bot"),
            BotCommand(command="menu", description="📱 Show main menu"),
        ]
        await self.bot.set_my_commands(commands)

    def setup_handlers(self):
        @self.dp.message(Command("menu"))
        async def cmd_menu(message: types.Message):
            await message.answer("📱Main menu", reply_markup=self.get_main_menu())

        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message, state: FSMContext):
            """Handler for /start command"""
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
            await message.answer("❌ Please enter a valid email address.")

        @self.dp.callback_query(F.data == "my_tasks")
        async def cmd_my_tasks(callback: types.CallbackQuery):
            messages = await get_user_tasks(callback.from_user.id)
            await callback.message.answer('📋 List of tasks')
            for message_text in messages:
                await callback.message.answer(message_text)
            await callback.answer()

        @self.dp.callback_query(F.data == "create_task")
        async def cmd_create_task(callback: types.CallbackQuery, state: FSMContext):
            await callback.message.answer('Input task title')
            await callback.answer()
            await state.set_state(Form.waiting_for_task_title)

        @self.dp.message(Form.waiting_for_task_title)
        async def task_title_input(message: types.Message, state: FSMContext):
            task_title = message.text
            await state.update_data(task_title=task_title)
            await message.answer('Input task description')
            await state.set_state(Form.waiting_for_task_description)

        @self.dp.message(Form.waiting_for_task_description)
        async def task_description_input(message: types.Message, state: FSMContext):
            task_description = message.text
            categories = await get_categories()
            await state.update_data(task_description=task_description)
            await message.answer('Input task category', reply_markup=categories)

        @self.dp.callback_query(F.data.startswith("category_"))
        async def task_category_input(callback: types.CallbackQuery, state: FSMContext):
            task_category = callback.data.split("_")[1]
            await state.update_data(task_category=task_category)
            await callback.answer()
            await callback.message.answer('Input task deadline')
            await state.set_state(Form.waiting_for_task_deadline)

        @self.dp.message(Form.waiting_for_task_deadline, F.text.regexp(r'^\d{2}.\d{2}.\d{4} \d{2}:\d{2}$'))
        async def task_deadline_input(message: types.Message, state: FSMContext):
            task_deadline = message.text
            await state.update_data(task_deadline=task_deadline)
            await self.create_task(message, state)  # ✅ Исправлен вызов

        @self.dp.message(Form.waiting_for_task_deadline)
        async def datetime_bad_input(message: types.Message, state: FSMContext):
            await message.answer('❌ Please enter valid datetime in format dd.mm.yyyy hh:mm')

        @self.dp.callback_query(F.data == "categories")
        async def show_categories(callback: types.CallbackQuery):
            categories = await get_categories('show_')
            await callback.message.answer('Tasks categories', reply_markup=categories)
            await callback.answer()

        @self.dp.callback_query(F.data.startswith("show_category_"))
        async def show_category_tasks(callback: types.CallbackQuery):
            category = callback.data.split("_")[2]
            messages = await get_user_tasks(callback.from_user.id, category)
            await callback.answer()
            if type(messages) == list:
                await callback.message.answer(f'📋 List of tasks in category {category}')
                for message_text in messages:
                    await callback.message.answer(message_text)
            else:
                await callback.message.answer(messages)

    async def create_task(self, message: types.Message, state: FSMContext):
        data = await state.get_data()
        task_data = {
            'title': data.get('task_title'),
            'description': data.get('task_description'),
            'category': data.get('task_category'),
            'deadline': data.get('task_deadline'),
        }
        answer_message, is_created = await save_task(task_data, message.from_user.id)
        await message.answer(answer_message)
        if is_created:
            await state.clear()

    async def start_polling(self):
        """Start bot in polling mode"""
        print("🤖 Telegram bot started")
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=10, force_close=True)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)

        await self.set_bot_commands()
        await self.dp.start_polling(self.bot)

    async def stop(self):
        """Корректное завершение работы"""
        if self.session and not self.session.closed:
            await self.session.close()
        if self.bot.session:
            await self.bot.session.close()