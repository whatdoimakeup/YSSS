from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from хранилка import хранилище


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /count - увеличить счетчик"""
    chat_id = update.effective_chat.id
    new_value = хранилище.увеличить_счетчик(chat_id)
    await update.message.reply_text(
        f"✅ Что то странное было сказано!\nВсего люди говорили что то странное: {new_value} раз/а."
    )


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stat - показать стату"""
    chat_id = update.effective_chat.id
    value = хранилище.получить_счетчик(chat_id)
    await update.message.reply_text(f"📊 Статистика: {value}")


def register_handlers(application: Application):
    """ЫЫЫЫЫЫЫЫЫЫЫЫЫЫ"""
    application.add_handler(CommandHandler("you_say_something_strange", count))
    application.add_handler(CommandHandler("stat", stat))
