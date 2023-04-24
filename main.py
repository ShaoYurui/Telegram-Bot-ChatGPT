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
    system_message = "You are a helpful chatbot using GPT-4. "
    user_prompt = "User: "
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=system_message + user_prompt + user_message,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
    )

    response = response.choices[0].text.strip()
    if "\n\n" in response:
        response = response.split("\n\n")[-1]

    return response


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a response from ChatGPT based on the user message."""
    user_message = update.message.text
    gpt_response = await generate_gpt_response(user_message)
    await update.message.reply_text(gpt_response)


if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()
