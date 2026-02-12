from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from хранилка import хранилище


async def ты_говоришь_что_то_странное(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Команда /count - увеличить счетчик"""
    chat_id = update.effective_chat.id
    new_value = хранилище.увеличить_счетчик(chat_id)
    await update.message.reply_text(
        f"✅ Что то странное было сказано!\nВсего люди говорили что то странное: {new_value} раз/а."
    )


async def статистика(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stat - показать стату"""
    chat_id = update.effective_chat.id
    value = хранилище.получить_счетчик(chat_id)
    await update.message.reply_text(f"📊 Статистика: {value}")


def регистратор_команд(робот: Application):
    """ЫЫЫЫЫЫЫЫЫЫЫЫЫЫ"""
    робот.add_handler(
        CommandHandler("you_say_something_strange", ты_говоришь_что_то_странное)
    )
    робот.add_handler(CommandHandler("stat", статистика))
