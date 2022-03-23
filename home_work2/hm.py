import logging
from lesson_2.config import *

from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import BotCommand, Update, ParseMode


def photo_video(update: Update, context: CallbackContext):
    update.message.reply_text("i've got your media file.\nhere it is:")
    message = update.message
    if message.photo:
        message.reply_photo(message.photo[-1])
    else:
        message.reply_video(message.video.file_id)


def audio(update: Update, context: CallbackContext):
    message = update.message
    message.reply_text("nice song bro.\nwould you like to listen it again?")
    message.reply_audio(message.audio.file_id)


def forwarded_photo_video(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(
        "*have i seen your media file before?*",
    )


def url(update: Update, context: CallbackContext):
    update.message.reply_text("isn't this link a scam?")


def save_number(update: Update, context: CallbackContext):
    message = update.message
    if len(context.args) < 2:
        message.reply_text("lack of arguments. write key and value.")
        return
    key, value = context.args[:2]
    context.user_data.update({key: value})
    message.reply_text("successfully added.")
    view_numbers(update, context)


def view_numbers(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"current user data:\n`{context.user_data}`",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def sum_numbers(update: Update, context: CallbackContext):
    total = 0
    if not context.args:
        update.message.reply_text("write some keys.")
        return
    for key in context.args:
        value = context.user_data.get(key, 0)
        try:
            total += int(value)
        except ValueError:
            continue
    update.message.reply_text(f"total: {total}")


def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text("unknown command.")


def random_message(update: Update, context: CallbackContext):
    update.message.reply_text("i don't understand you.")


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    updater.bot.set_my_commands([
        BotCommand("number", "[key] [value] save value with key in user_data"),
        BotCommand("sum", "[key1] ... sum values of keys from user_data"),
        BotCommand("view", "view current user_data"),
    ])

    dispatcher.add_handler(CommandHandler("number", save_number))
    dispatcher.add_handler(CommandHandler("sum", sum_numbers))
    dispatcher.add_handler(CommandHandler("view", view_numbers))

    dispatcher.add_handler(
        MessageHandler((Filters.photo | Filters.video) & Filters.forwarded,
                       forwarded_photo_video))
    dispatcher.add_handler(
        MessageHandler(Filters.photo | Filters.video, photo_video))
    dispatcher.add_handler(
        MessageHandler(Filters.audio, audio))
    dispatcher.add_handler(
        MessageHandler(Filters.entity("url"), url))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    dispatcher.add_handler(MessageHandler(Filters.all, random_message))

    updater.start_polling()


if __name__ == "__main__":
    main()