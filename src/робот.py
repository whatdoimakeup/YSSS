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
    "denis_are_you_with_us": "Денис, ты с нами?",
    "danchistyakov_are_you_with_us": "Даня, ты с нами?",
    "danya_gorev_is_late": "Даня Горев, видимо, опаздывает",
    "managers_keep_coming": "В меня постоянно ходят менеджеры",
    "let_me_tell_about_myself": "Расскажу пару слов о себе",
    "dont_forget_weekend": "Не забудьте уйти на выходные",
    "meeting_start_at_11": "Старт встречи в 11:00",
    "meeting_start_at_1115": "Старт встречи в 11:15",
    "govnokod": "Говнoкод",
    "magic": "Магия"
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
