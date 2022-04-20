import re

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

from user_commands import *
from admin_commands import *

from buttons_commands import *


def command_handler(dispatcher):
    # User commands
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(MessageHandler(Filters.regex("Помощь"), help))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(MessageHandler(Filters.regex("Профиль"), my_profile))
    dispatcher.add_handler(CommandHandler("profile", my_profile))

    dispatcher.add_handler(MessageHandler(Filters.regex("Мои заказы"), my_orders))
    dispatcher.add_handler(CommandHandler("myorders", my_orders))

    # New order
    new_order_handler = ConversationHandler(
        entry_points=[CommandHandler('neworder', new_order), MessageHandler(Filters.regex("Новый заказ"), new_order)],
        states={
            0: [CallbackQueryHandler(pattern=r'@doneproducts', callback=address)],
            1: [MessageHandler(Filters.text, phone)],
            2: [MessageHandler(Filters.text, finish_order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(new_order_handler)

    # Admin commannds
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("adminhelp", adminhelp))
    dispatcher.add_handler(CommandHandler("getorder", getorder))
    dispatcher.add_handler(CommandHandler("getuser", getuser))

    # Buttons
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    # Utils
    dispatcher.add_handler(MessageHandler(Filters.text, all_messages))
