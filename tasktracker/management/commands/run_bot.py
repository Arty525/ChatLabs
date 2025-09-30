from django.core.management.base import BaseCommand
import asyncio
from bot.bot import TelegramBot


class Command(BaseCommand):
    help = 'Запускает Telegram бота для работы с моделью Customer'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Запуск Telegram бота'))

        bot = TelegramBot()

        try:
            asyncio.run(bot.start_polling())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('⏹️ Бот остановлен'))