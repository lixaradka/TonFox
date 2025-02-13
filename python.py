import os
import base64
import requests
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
TELEGRAM_TOKEN = "8092687951:AAGp4a-h-CYi4eVn-pqF9cXjjK49gVj2K-M"
STABILITY_API_KEY = "sk-BfNK4kYxvgkv0BQVd0o1Tq1BF6h0MSp2rwAgWC0av9S1kdu2"


# Инициализация
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Хранение данных пользователей
user_data = {}

# Команда /start
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Открыть галерею", web_app={"url": "https://tonfox-lixaradka-lixaradkas-projects.vercel.app/"})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔮 Добро пожаловать в Цифрового Алхимика!\n"
        "Отправьте текст, чтобы создать NFT-артефакт.",
        reply_markup=reply_markup
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context):
    text = update.message.text
    user_id = update.message.from_user.id

    if not text:
        await update.message.reply_text("Пожалуйста, отправьте текстовое сообщение.")
        return

    try:
        # Генерация изображения
        image_url = await generate_image(text)
        
        # Обновление данных пользователя
        await update_user_data(user_id, xp=10)
        
        # Отправка результата
        await update.message.reply_photo(
            photo=image_url,
            caption=f"🎨 Ваш артефакт создан!\n"
                    f"🔗 Просмотреть: {image_url}"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

# Генерация изображения через Stability AI
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

async def generate_image(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Stability API Error: {response.text}")

    # Сохранение изображения
    image_data = response.json()["artifacts"][0]["base64"]
    image_bytes = base64.b64decode(image_data)
    image_file = BytesIO(image_bytes)
    image_file.name = f"artifact_{int(time.time())}.png"  # Уникальное имя файла

    # Сохраняем изображение на сервере
    with open(os.path.join(UPLOAD_FOLDER, image_file.name), 'wb') as f:
        f.write(image_file.getvalue())

    return f"/{UPLOAD_FOLDER}/{image_file.name}"


# Обновление данных пользователя
async def update_user_data(user_id, xp=0):
    if user_id not in user_data:
        user_data[user_id] = {"xp": 0, "level": 1}
    user_data[user_id]["xp"] += xp
    if user_data[user_id]["xp"] >= 100 * user_data[user_id]["level"]:
        user_data[user_id]["level"] += 1
        await app.bot.send_message(
            chat_id=user_id,
            text=f"🎉 Поздравляем! Вы достигли уровня {user_data[user_id]['level']}!"
        )

# Команда для покупки кредитов
async def buy_credits(update: Update, context):
    await update.message.reply_invoice(
        title="Покупка кредитов",
        description="100 кредитов для генерации изображений",
        payload="100_credits",
        provider_token="YOUR_PROVIDER_TOKEN",  # Получите у платежного провайдера
        currency="USD",
        prices=[{"label": "100 Credits", "amount": 500}]  # $5.00
    )

# Обработка успешного платежа
async def handle_successful_payment(update: Update, context):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"credits": 0}
    user_data[user_id]["credits"] += 100
    await update.message.reply_text("✅ Платеж успешен! Ваши кредиты добавлены.")

# Регистрация обработчиков
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("buy", buy_credits))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_successful_payment))

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    app.run_polling()


