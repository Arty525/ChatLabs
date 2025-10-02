from django.core.management.base import BaseCommand
import asyncio
import signal
import sys
from bot.bot import TelegramBot


class Command(BaseCommand):
    help = "Запускает Telegram бота для работы с моделью Customer"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Запуск Telegram бота"))

        bot = TelegramBot()

        async def main():
            try:
                await bot.start_polling()
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("⏹️ Получен сигнал прерывания"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Ошибка: {e}"))
            finally:
                await bot.stop()
                self.stdout.write(self.style.SUCCESS("✅ Бот корректно остановлен"))

        def signal_handler(sig, frame):
            print("\n🛑 Получен сигнал завершения...")
            asyncio.create_task(bot.stop())
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("⏹️ Бот остановлен"))
