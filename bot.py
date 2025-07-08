from database import SessionLocal
from models import User
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your bot.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    tg_user = update.effective_user

    existing = db.query(User).filter(User.username == tg_user.username).first()
    if not existing:
        new_user = User(username=tg_user.username)
        db.add(new_user)
        db.commit()

    db.close()

    await update.message.reply_text("You’ve been added to the system!")
    
