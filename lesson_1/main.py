# Импортируем все необходимое
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext

import logging

TOKEN = ""  # Тут ваш токен из BotFather

updater = Updater(token=TOKEN)  # Создаем updater
dispatcher = updater.dispatcher  # Создаем dispatcher

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


# Вызывется при нажатии кнопки "Start"
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello world!")
    print(context.args)


# /sum
def sum(update, context):
    args = context.args
    try:
        a = int(args[0])
        b = int(args[1])
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Numbers must be int!")
        return 0
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Result is {int(args[0]) + int(args[1])}")


# /caps
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# text
def text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I don't understand you")


start_handler = CommandHandler('start', start)  # Создаем handler для /start
sum_handler = CommandHandler('sum', sum)  # Создаем handler для /sum
caps_handler = CommandHandler('caps', caps)  # Создаем handler для /caps
text_handler = MessageHandler(Filters.text, text)  # Создаем handler для text


dispatcher.add_handler(start_handler)  # Добавляем handler start_handler
dispatcher.add_handler(sum_handler)  # Добавляем handler sum_handler
dispatcher.add_handler(caps_handler)  # Добавляем handler caps_handler
dispatcher.add_handler(text_handler)  # Добавляем handler text_handler
dispatcher.add_handler(text_handler)  # Добавляем handler text_handler

updater.start_polling()  # Запускаем updater
