import logging
from telegram import Update
import openai
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Set up OpenAI API key
openai.api_key = ""

# Set up Telegram API token
TELEGRAM_API_TOKEN = ""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def generate_gpt_response(user_message: str):
    system_message = "You are a helpful chat bot"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_message}]
    )

    return response.choices[0].message.content


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a response from ChatGPT based on the user message."""
    user_message = update.message.text
    gpt_response = await generate_gpt_response(user_message)
    await update.message.reply_text(gpt_response)


if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()
