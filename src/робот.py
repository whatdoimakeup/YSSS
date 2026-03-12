import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from tortoise.functions import Count
from src.хранилка import хранилище
from src.models import User, Счетчик

КОМАНДЫ = {
    "you_say_something_strange": "Ты говоришь что то странное",
    "risks": "Риски",
    "kirill_not_drinking": "Кирилл отказался пить пиво",
    "what_do_you_mean": "О чем ты вообще?",
    "i_dont_understand_you": "Я тебя не понимаю",
    "same_but_slower": "То же самое, но медленнее",
    "not_answering_a_question": "Ты не отвечаешь на вопрос",
    "meet_longer_than_two_hours": "Мит более 2 часов",
    "danil_chudin": "Даня Чудин",
    "call_bingo": "Зов на дейли",
    "denis_are_you_with_us": "Денис, ты с нами?",
    "danchistyakov_are_you_with_us": "Даня, ты с нами?",
    "danya_gorev_is_late": "Даня Горев, видимо, опаздывает",
    "managers_keep_coming": "В меня постоянно ходят менеджеры",
    "let_me_tell_about_myself": "Расскажу пару слов о себе",
    "dont_forget_weekend": "Не забудьте уйти на выходные",
    "meeting_start_at_11": "Старт встречи в 11:00",
    "meeting_start_at_1115": "Старт встречи в 11:15",
    "govnokod": "Говнoкод",
    "magic": "Магия",
    "take_your_fav_drink": "Возьмите свой любимый напиток",
    "clear_value": "Понятная ценность",
    "story_from_technopark": "Вот историю одну из своего опыта расскажу, ещё из Технопарка",
}


async def счетчик(update: Update, context: ContextTypes.DEFAULT_TYPE, bucket: str):
    """Команда для увеличения счетчика"""
    chat_id = update.effective_chat.id
    author = await User.from_telegram_user(update.effective_user)

    новый_счетчик = await хранилище.добавить_счетчик(chat_id, author, bucket)
    новое_значение = await хранилище.получить_счетчик(chat_id, bucket)

    keyboard = [[InlineKeyboardButton("Отминет", callback_data=f"cancel_{новый_счетчик.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ Записали ✍️: {КОМАНДЫ[bucket]}: {новое_значение}\nСпасибо, {author.user_mention}!",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )


async def contributors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать всех контрибьюторов"""
    chat_id = update.effective_chat.id
    counters = (
        await Счетчик.filter(chat_id=chat_id, is_active=True, author_id__not_isnull=True)
        .annotate(total=Count("id"))
        .group_by("author_id")
        .order_by("-total")
        .values("author_id", "total")
    )

    if not counters:
        await update.message.reply_text("👥 Контрибьюторов пока нет")
        return

    author_ids = [counter["author_id"] for counter in counters]
    authors = await User.filter(id__in=author_ids)
    authors_by_id = {author.id: author for author in authors}

    контрибьюторы = "\n".join(
        [
            f"{authors_by_id.get(counter['author_id']).user_mention}: {counter['total']}"
            for counter in counters
            if counter["author_id"] in authors_by_id
        ]
    )
    await update.message.reply_text(f"👥 Контрибьюторы:\n{контрибьюторы}", parse_mode="HTML")


async def отменить_счетчик(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отминет делать"""
    query = update.callback_query
    await query.answer()

    # Получаем bucket из callback_data
    id_счетчика = query.data.replace("cancel_", "")
    chat_id = update.effective_chat.id

    # Уменьшаем счетчик на 1
    await хранилище.уменьшить_счетчик(chat_id, id_счетчика)

    await query.edit_message_text(text="❌ Отменено")


async def статистика(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stat - показать стату"""
    chat_id = update.effective_chat.id
    value = await хранилище.получить_все_счетчики(chat_id)
    статистика_текста = "\n".join(
        [f"{КОМАНДЫ.get(k, 'WTF???')}: {v}" for k, v in sorted(value.items(), key=lambda x: x[1], reverse=True)]
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
        робот.add_handler(CommandHandler(bucket, lambda u, c, b=bucket: счетчик(u, c, b)))
    робот.add_handler(CallbackQueryHandler(отменить_счетчик, pattern="^cancel_"))
    робот.add_handler(CommandHandler("stat", статистика))
    робот.add_handler(CommandHandler("commands", счетчики))
    робот.add_handler(CommandHandler("bingo", бинго))
    робот.add_handler(CommandHandler("contributors", contributors))
