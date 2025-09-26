# THENEXTMIXTAPE TELEGRAM BOT
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

if os.getenv("RENDER") is None:
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Переменная TELEGRAM_BOT_TOKEN не задана! Проверь .env или переменные окружения.")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

EVERYMOTIONS_WORDS = {
    'AI': 'искусственный интеллект (artificial intelligence)',
    'truth': 'правда',
    'circuits': 'технологические или электрические схемы',
    'awake': 'пробуждаться/просыпаться',
    'glitch': 'глитч',
    'groove': 'грув, т.е. ритмическая "проработка" трека',
    'embrace': 'принимать',
    'trace': 'след, т.е. оставить что-то после себя'
}

DAYBYDAY_WORDS = {
    'solos': 'гитарные соло (guitar solos)',
    'rolls': 'барабанные партии (drum rolls)',
    'compile': 'компилировать, т.е. писать код в программе-компиляторе',
    'vibe': 'вайб, т.е. эмоциональная атмосфера',
    'stage': 'музыкальная сцена',
    'mic': 'микрофон (microphone)',
    'screaming crowd': 'кричащая толпа (на концерте)',
    'syntax': 'синтакс, т.е. набор правил, обозначений и соглашений для написания верного кода в программе',
    'core': 'ядро системы, т.е. внутренняя сущность кода или нынешнего творчества',
    'beats': 'биты, т.е. инструменталы в современной музыке',
    'mode': 'режим работы',
    'life-hit': '"хит жизни", т.е. занятие, определяющее жизнь',
    'doubt': 'сомнение в чём-либо'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📖 Every Motions (Глоссарий)")],
        [KeyboardButton("📅 Day By Day (Глоссарий)")],
        [KeyboardButton("❌ Завершить")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "=== THENEXTMIXTAPE ===\n"
        "Англо-русский глоссарий\n\n"
        "Выберите раздел для изучения:"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📖 Every Motions (Глоссарий)":
        context.user_data["mode"] = "every_motions"
        words_list = "\n".join([f"• {word}" for word in EVERYMOTIONS_WORDS.keys()])
        await update.message.reply_text(
            "📚 Раздел: Every Motions\n\n"
            "Доступные слова:\n"
            f"{words_list}\n\n"
            "Введите слово для перевода."
        )
        
    elif text == "📅 Day By Day (Глоссарий)":
        context.user_data["mode"] = "daybyday"
        words_list = "\n".join([f"• {word}" for word in DAYBYDAY_WORDS.keys()])
        await update.message.reply_text(
            "📅 Раздел: Day By Day\n\n"
            "Доступные слова:\n"
            f"{words_list}\n\n"
            "Введите слово для перевода."
        )
        
    elif text == "❌ Завершить":
        context.user_data.pop("mode", None)
        await update.message.reply_text("👋 До свидания! Возвращайтесь снова!")
        await start(update, context)
        
    else:
        await handle_word_translation(update, context, text)

async def handle_word_translation(update: Update, context: ContextTypes.DEFAULT_TYPE, word: str = None):
    if word is None:
        word = update.message.text.strip()
    
    mode = context.user_data.get("mode")
    
    if mode == "every_motions":
        translation = EVERYMOTIONS_WORDS.get(word)
        if translation:
            await update.message.reply_text(f"🔤 {word}\n🇷🇺 {translation}")
        else:
            words_list = "\n".join([f"• {w}" for w in EVERYMOTIONS_WORDS.keys()])
            await update.message.reply_text(
                f"❌ Слово '{word}' не найдено в Every Motions.\n\n"
                f"Доступные слова:\n{words_list}"
            )
            
    elif mode == "daybyday":
        translation = DAYBYDAY_WORDS.get(word)
        if translation:
            await update.message.reply_text(f"🔤 {word}\n🇷🇺 {translation}")
        else:
            words_list = "\n".join([f"• {w}" for w in DAYBYDAY_WORDS.keys()])
            await update.message.reply_text(
                f"❌ Слово '{word}' не найдено в Day By Day.\n\n"
                f"Доступные слова:\n{words_list}"
            )
    else:
        await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 THENEXTMIXTAPE - Глоссарий\n\n"
        "1. Выберите раздел\n"
        "2. Введите слово\n"
        "Команды: /start, /help"
    )

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_choice))
    
    print("✅ Бот запущен! Не закрывай это окно.")
    application.run_polling()

if __name__ == '__main__':
    main()