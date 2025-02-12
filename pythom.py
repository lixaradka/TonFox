from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем кнопку для открытия мини-приложения
    keyboard = [
        [InlineKeyboardButton("Открыть мини-приложение", web_app=WebAppInfo(url="https://tonfox-lixaradka-lixaradkas-projects.vercel.app/"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    await update.message.reply_text("Нажмите кнопку, чтобы открыть мини-приложение:", reply_markup=reply_markup)

# Основная функция для запуска бота
def main():
    # Создаем приложение бота с вашим токеном
    app = ApplicationBuilder().token("8092687951:AAGp4a-h-CYi4eVn-pqF9cXjjK49gVj2K-M").build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()