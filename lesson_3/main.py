import logging

import telegram
from telegram import Update, ForceReply, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, \
    InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, Defaults, CallbackQueryHandler
from typing import Union, List
from telegram import InlineKeyboardButton

# Enable logging
from lesson_2.config import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu


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


def media(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    media1 = InputMediaPhoto(media=open('media/photo.jpg', 'rb'))
    media2 = InputMediaPhoto(media='http://s.ekabu.ru/localStorage/post/13/eb/be/98/13ebbe98_resizedScaled_740to493.gif')

    context.bot.send_media_group(chat_id=update.effective_chat.id, media=[media1, media2])


def reply_buttons(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        ['Button 1', 'Button 2'],
        ['Button 3', 'Button 4', 'Button 5']
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Reply keyboard", reply_markup=reply_markup)


def clear(update: Update, context: CallbackContext) -> None:
    reply_keyboard = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Clear", reply_markup=reply_keyboard)


def inline_keyboard(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        [
            InlineKeyboardButton('Click me!', callback_data='0'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Count: ", reply_markup=reply_markup)


def btn_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    count = int(query.data) + 1
    custom_keyboard = [
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
        InlineKeyboardButton('Click me!', callback_data=count),
    ]
    header_keyboard = [
        InlineKeyboardButton('Click', callback_data=count),
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(buttons=custom_keyboard, n_cols=2, header_buttons=header_keyboard))
    query.edit_message_text(text=f"Count: {count}", reply_markup=reply_markup)


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
    dispatcher.add_handler(CommandHandler("media", media))
    dispatcher.add_handler(CommandHandler("rbuttons", reply_buttons))
    dispatcher.add_handler(CommandHandler("ibuttons", inline_keyboard))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
