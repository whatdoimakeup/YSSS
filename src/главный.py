import os
from telegram import Update
from telegram.ext import Application

from робот import регистратор_команд


def запуск():
    """Запуск бота"""
    # Замените 'YOUR_TOKEN' на токен вашего бота
    ключ = os.getenv("TELEGRAM_BOT_TOKEN", None)
    if not ключ:
        print("Ошибка: TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
        return

    робот = Application.builder().token(ключ).build()
    регистратор_команд(робот)

    print("Бот запущен и ждет пока кто то скажет что то странное...")
    робот.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    запуск()
