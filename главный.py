import os
from telegram import Update
from telegram.ext import Application
from tortoise import Tortoise
from tortoise.context import TortoiseContext

from src.робот import регистратор_команд
from src.хранилка import TORTOISE_ORM


async def при_старте(_app: Application):
    await Tortoise.init(config=TORTOISE_ORM)


async def при_остановке(_app: Application):
    await Tortoise.close_connections()


def запуск():
    """Запуск бота"""
    ключ = os.getenv("TELEGRAM_BOT_TOKEN", None)
    if not ключ:
        print("Ошибка: TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
        return

    робот = Application.builder().token(ключ).post_init(при_старте).post_shutdown(при_остановке).build()
    регистратор_команд(робот)
    print("Бот запущен и ждет пока кто то скажет что то странное...")
    with TortoiseContext():
        робот.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    запуск()
