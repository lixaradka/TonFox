from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Обработчик команды /start


def main():
    # Создаем приложение бота с вашим токеном
    app = ApplicationBuilder().token("8092687951:AAGp4a-h-CYi4eVn-pqF9cXjjK49gVj2K-M").build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start")) 

    app.run_polling()

if __name__ == "__main__":
    main()