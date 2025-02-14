import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
QUESTIONS, PHONE = range(2)

# ID группы, куда отправляются данные
GROUP_CHAT_ID = -4631460753

# Клавиатуры
start_keyboard = ReplyKeyboardMarkup([["📜 Мои объявления"]], resize_keyboard=True)
main_keyboard = ReplyKeyboardMarkup(
    [["📜 Мои объявления", "⬅️ Назад"]], resize_keyboard=True
)
phone_keyboard = ReplyKeyboardMarkup(
    [["📜 Мои объявления", "⬅️ Назад"]], resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Старт диалога."""
    context.user_data.setdefault("phones", [])  # Инициализируем список телефонов

    await update.message.reply_text(
        "Привет! Это бот для аренды WhatsApp аккаунтов.\n"
        "Ответьте на вопросы:\n"
        "1. Когда был создан аккаунт?\n"
        "2. Насколько активен аккаунт?\n\n"
        "Введите ответы через запятую.",
        reply_markup=main_keyboard,
    )
    return QUESTIONS


async def get_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем ответы и просим ввести номер телефона."""
    text = update.message.text

    if text == "📜 Мои объявления":
        return await list_phones(update, context)

    if text == "⬅️ Назад":
        return await start(update, context)

    context.user_data["answers"] = text

    await update.message.reply_text(
        "❤️ Спасибо! Теперь введите ваш номер телефона.📞\n\n"
        "🛡️ Мы не имеем доступа к вашему аккаунту.\n"
        "🔏 Ваши данные не передаются третьим лицам.",
        reply_markup=phone_keyboard,
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняем номер телефона и отправляем данные в группу."""
    text = update.message.text

    if text == "⬅️ Назад":
        await update.message.reply_text(
            "🔙 Вернулись назад. Введите ответы на вопросы.", reply_markup=main_keyboard
        )
        return QUESTIONS

    if text == "📜 Мои объявления":
        return await list_phones(update, context)

    # Сохраняем номер в список
    context.user_data["phones"].append(text)

    # Получаем данные пользователя
    user = update.message.from_user
    username = user.username
    user_identifier = f"@{username}" if username else f"ID: {user.id}"

    # Отправляем данные в группу
    message = (
        f"📌 Новый запрос:\n"
        f"👤 Пользователь: {user_identifier}\n"
        f"📋 Ответы: {context.user_data.get('answers')}\n"
        f"📱 Номер телефона: {text}"
    )

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)

    await update.message.reply_text(
        "✅ Ваши данные отправлены! Мы с вами свяжемся как можно быстрее.",
        reply_markup=start_keyboard,
    )

    return ConversationHandler.END


async def list_phones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправляет пользователю список его отправленных номеров."""
    phones = context.user_data.get("phones", [])

    if not phones:
        await update.message.reply_text("📭 Вы ещё не отправили ни одного номера.", reply_markup=main_keyboard)
    else:
        phone_list = "\n".join(phones)
        await update.message.reply_text(f"📜 Ваши объявления:\n{phone_list}", reply_markup=main_keyboard)

    return QUESTIONS if update.message.text == "📜 Мои объявления" else PHONE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена операции."""
    await update.message.reply_text(
        "🚫 Операция отменена. Отправьте /start для начала заново.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    """Запуск бота."""
    application = Application.builder().token("7941700806:AAGCClSoFdHWwV1c4u5YVpMT3-9qFokGV4Y").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_questions)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()


