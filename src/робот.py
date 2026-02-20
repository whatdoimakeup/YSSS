import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from хранилка import хранилище

КОМАНДЫ = {
    "you_say_something_strange": "Ты говоришь что то странное",
    "risks": "Риски",
    "kirill_not_drinking": "Кирилл отказался пить пиво",
    "what_do_you_mean": "О чем ты вообще?",
    "i_dont_understand_you": "Я тебя не понимаю",
    "same_but_slower": "То же самое, но медленнее",
    "not_answering_a_question": "Ты не отвечаешь на вопрос",
    "meet_longger_than_two_hours": "Мит более 2 часов",
    "danil_chudin": "Даня Чудин",
    "bingo": "Зов на дейли",
}


async def счетчик(update: Update, context: ContextTypes.DEFAULT_TYPE, bucket: str):
    """Команда для увеличения счетчика"""
    chat_id = update.effective_chat.id
    new_value = хранилище.увеличить_счетчик(chat_id, bucket)

    keyboard = [[InlineKeyboardButton("Отминет", callback_data=f"cancel_{bucket}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ Записали ✍️: {КОМАНДЫ[bucket]}: {new_value}", reply_markup=reply_markup
    )


async def отменить_счетчик(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отминет делать"""
    query = update.callback_query
    await query.answer()

    # Получаем bucket из callback_data
    bucket = query.data.replace("cancel_", "")
    chat_id = update.effective_chat.id

    # Уменьшаем счетчик на 1
    new_value = хранилище.уменьшить_счетчик(chat_id, bucket)

    await query.edit_message_text(text=f"❌ Отменено: {КОМАНДЫ[bucket]}: {new_value}")


async def статистика(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stat - показать стату"""
    chat_id = update.effective_chat.id
    value = хранилище.получить_все_счетчики(chat_id)
    статистика_текста = "\n".join(
        [
            f"{КОМАНДЫ.get(k, 'WTF???')}: {v}"
            for k, v in sorted(value.items(), key=lambda x: x[1], reverse=True)
        ]
    )
    await update.message.reply_text(f"📊 Статистика:\n{статистика_текста}")


async def счетчики(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать все счетчики"""
    счетчики_текста = "\n".join([f"/{k}: {v}" for k, v in КОМАНДЫ.items()])
    await update.message.reply_text(f"📊 Все счетчики:\n{счетчики_текста}")


async def бинго(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для генерации сообщения о встрече"""
    время = random.choice(["11:00", "11:05", "11:10"])

    проекты = ["AllCups", "Study", "GTP"]
    random.shuffle(проекты)
    рандомное_число_для_напитка = random.randint(0, 100)
    рандомное_число_для_задач = random.randint(0, 100)
    сегодня_пятница = datetime.now().weekday() == 4

    сообщение = (
        f"Всем привет, коллеги!\n"
        f"Сегодня старт встречи в {время}. "
        f"Обсудим {проекты[0]}, затем {проекты[1]} и в конце {проекты[2]}"
    )
    if сегодня_пятница and рандомное_число_для_задач > 50:
        сообщение += "\nПосмотрите задачи, которые можно закрыть"
    if сегодня_пятница and рандомное_число_для_напитка > 80:
        сообщение += "\nВозьмите свой любимый напиток!"

    await update.message.reply_text(сообщение)


def регистратор_команд(робот: Application):
    """ЫЫЫЫЫЫЫЫЫЫЫЫЫЫ"""
    for bucket in КОМАНДЫ.keys():
        print(f"Регистрируем команду: {bucket}")
        робот.add_handler(
            CommandHandler(bucket, lambda u, c, b=bucket: счетчик(u, c, b))
        )
    робот.add_handler(CallbackQueryHandler(отменить_счетчик, pattern="^cancel_"))
    робот.add_handler(CommandHandler("stat", статистика))
    робот.add_handler(CommandHandler("commands", счетчики))
    робот.add_handler(CommandHandler("bingo", бинго))
