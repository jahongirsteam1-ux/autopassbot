"""
Auto Chek Bot — Telegram Bot
Mini App launcher + admin commands
"""

import os, logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-app.netlify.app")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🚀 Tizimga kirish", web_app=WebAppInfo(url=MINI_APP_URL))
    ]])
    
    # Xabarni yanada chiroyli va tushunarli qilib HTML formatida yozdim
    text = (
        f"<b>👋 Salom, {u.first_name}!</b>\n\n"
        "<b>Auto Chek Bot</b> ga xush kelibsiz.\n"
        "Men sizning operatsiyalaringizni avtomatlashtirish va "
        "monitoring qilishda yordam beraman.\n\n"
        "<i>Tizimga kirish uchun quyidagi tugmani bosing:</i>"
    )
    
    await update.message.reply_text(
        text, 
        parse_mode="HTML", 
        reply_markup=kb
    )

async def post_init(app):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="🚀 Ochish", web_app=WebAppInfo(url=MINI_APP_URL))
    )

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
