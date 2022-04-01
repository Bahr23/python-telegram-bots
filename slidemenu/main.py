import logging

import telegram
from telegram import Update, ForceReply, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, \
    InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, Defaults, CallbackQueryHandler
from typing import Union, List
from telegram import InlineKeyboardButton

# Enable logging
from config import *
from menus import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def slide_menu(update: Update, context: CallbackContext) -> None:
    menu = get_menu("slidemenu")
    context.bot.send_message(chat_id=update.effective_chat.id, text=menu.text, reply_markup=menu.reply_markup)


def btn_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data[0] == '#':
        menu = get_menu(query.data)
        query.edit_message_text(text=menu.text, reply_markup=menu.reply_markup)
    else:
        query.answer(text=query.data)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    defaults = Defaults(parse_mode=ParseMode.HTML)

    TOKEN = ''

    updater = Updater(TOKEN, defaults=defaults)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("slidemenu", slide_menu))
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
