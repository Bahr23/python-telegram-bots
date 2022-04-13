import telegram

from core import *
from config import *


@checkuser
def admin(update, context):
    user = User.get(id=update.message.from_user.id)

    if len(context.args) == 0:
        if user.status == 'admin':
            user.status = 'user'
            user.save()
            text = "Вы изменили ваш статус на user."
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        if context.args[0] == ADMIN_PASSWORD:
            user.status = 'admin'
            user.save()
            text = "Вы изменили ваш статус на admin."
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)


@checkuser
@checkadmin
def adminhelp(update, context):
    user = User.get(id=update.message.from_user.id)
    if user:
        if user.status == 'admin':
            text = '<b>Список комманд:</b>\n' \
                   '<code>/admin</code> - переключение между статусом пользователя/админа\n' \
                   '<code>/getorder</code> - управление заказом\n' \
                   '<code>/getuser</code> - посмотреть профиль пользователя\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)


@checkuser
@checkadmin
def getorder(update, context):
    try:
        order = Order.get(id=context.args[0])
        if not order:
            raise
        text = get_order(order, user=True)
        reply_markup = get_order_buttons(order)

    except Exception as e:
        print(e)
        text = "Используйте /get_order order_id или заказ не найден."
        reply_markup = None
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=reply_markup,
                             parse_mode=telegram.ParseMode.HTML)


@checkuser
@checkadmin
def getuser(update, context):
    try:
        find_user = User.get(id=int(context.args[0]))
        if not find_user:
            raise
        text = get_profile(find_user)
        reply_markup = get_user_buttons(find_user)
    except:
        text = "Используйте /get_user user_id или заказ не найден."
        reply_markup = None
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)