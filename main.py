import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
AI_API_KEY = os.environ["AI_API_KEY"]

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        # Send message to AI model (OpenAI or Gemini)
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": user_msg}],
            },
        )
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
