import os
import logging
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# تعيين التوكن لمفتاح بوت تيليجرام
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# الرد على الرسائل
def start(update, context):
    update.message.reply_text('مرحبًا! كيف يمكنني مساعدتك اليوم؟')

def help(update, context):
    update.message.reply_text('يمكنك طرح أي سؤال وسأجيب باستخدام OpenAI.')

def gpt_response(update, context):
    user_message = update.message.text
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        update.message.reply_text(response.choices[0].text.strip())
    except Exception as e:
        update.message.reply_text('حدث خطأ، حاول لاحقًا.')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # أوامر البوت
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt_response))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
