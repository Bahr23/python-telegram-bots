import telegram

from models import *
from core import *


def btn_handler(update, context):
    query = update.callback_query
    data = query.data.split("@")[1:]

    if data[0] == 'add_product':
        product = Product.get(id=data[1])
        if 'products' in context.user_data:
            context.user_data['products'].append(data[1])
        else:
            context.user_data['products'] = [data[1]]

        text = f'Вы добавили {product.name} в заказ.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    if data[0] == 'order':
        order = Order.get(id=data[1])
        text = get_order(order)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)

    if data[0] == 'adminorder':
        order = Order.get(id=data[1])
        text = get_order(order, True)
        reply_markup = get_order_buttons(order)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup
        )

    if data[0] == 'confirm':
        order = Order.get(id=int(data[1]))
        order.status = 'Принят'
        order.save()

        context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            reply_markup=get_order_buttons(order)
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы успешно приняли заказ!',
            parse_mode=telegram.ParseMode.HTML,
        )
        context.bot.send_message(
            chat_id=order.user.id,
            text=f'Заказ {order.id} принят и скоро прибудет к вам!',
            parse_mode=telegram.ParseMode.HTML,
        )
    if data[0] == 'complete':
        order = Order.get(id=int(data[1]))
        order.status = 'Завершен'
        order.save()

        context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            reply_markup=get_order_buttons(order)
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы успешно завершили заказ!',
            parse_mode=telegram.ParseMode.HTML,
        )
        context.bot.send_message(
            chat_id=order.user.id,
            text=f'Заказ {order.id} завершен!',
            parse_mode=telegram.ParseMode.HTML,
        )
    if data[0] == 'delete':
        order = Order.get(id=int(data[1]))

        context.bot.edit_message_reply_markup(
            chat_id=update.effective_chat.id,
            message_id=query.message.message_id,
            reply_markup=None
        )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы успешно удалил заказ!',
            parse_mode=telegram.ParseMode.HTML,
        )
        context.bot.send_message(
            chat_id=order.user.id,
            text=f'Заказ {order.id} удален!',
            parse_mode=telegram.ParseMode.HTML,
        )
        order.delete_instance()

    if data[0] == 'userorders':
        user = User.get(id=data[1])
        if user:
            orders = get_user_orders(user, True)
            text = f'Заказы пользовтеля #<code>{user.id}</code>:\n' + orders.text
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=telegram.ParseMode.HTML,
                reply_markup=orders.reply_markup
            )