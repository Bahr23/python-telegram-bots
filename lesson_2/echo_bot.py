import logging

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Defaults

# Enable logging
from lesson_2.config import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
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


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # update.message.reply_text(update.message.text)
    a = update
    b = context
    text = f"<code>{update.message.text}</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def video(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Video')


def photo_or_audio(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Photo or Audio')


def audio(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('Audio')


def put(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    key = 'key1'
    value = context.args[0]
    print(context.user_data)
    context.user_data[key] = value
    print(context.user_data)
    update.message.reply_text(key)


# /get key
def get(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    key = context.args[0]
    if key in context.user_data:
        update.message.reply_text(context.user_data[key])
    else:
        update.message.reply_text("Error")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(TOKEN, defaults=defaults)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("put", put))
    dispatcher.add_handler(CommandHandler("get", get))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.video, video))
    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.audio, photo_or_audio))
    # dispatcher.add_handler(MessageHandler(Filters.audio, audio))

    # & - and
    # | - or
    # ~ - not
    # ^ - xor

    # Filters.text, Filters.video, Filters.photo, Filters.audio, Filters.document
    # Filters.forwarded
    # Filters.entity(MessageEntity.URL)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()