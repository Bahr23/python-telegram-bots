import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler


from menus import *
from core import *


@checkuser
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")


@checkuser
def help(update, context):
    text = '<b>Список комманд:</b>\n'\
          '<code>/profile</code> - посмотреть свой профиль\n'\
          '<code>/neworder</code> - создать заказ\n'\
          '<code>/myorders</code> - посмотреть свои заказы\n'

    menu = get_menu('main')

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=menu.reply_markup,
                             parse_mode=ParseMode.HTML)


@checkuser
def all_messages(update, context):
    text = "Я не знаю как на это ответить. Воспользуйтесь разделом 'Помощь' (/help)"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=get_menu('main').reply_markup,
                             parse_mode=ParseMode.HTML)


@checkuser
def my_profile(update, context):
    user = User.get(id=update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=get_profile(user),
                             parse_mode=ParseMode.HTML)


# New order
@checkuser
def cancel(update, context):
    text = 'Создание заказа отменено'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


# @checkuser
def new_order(update, context):
    text = 'Выберите пункты меню:\n'

    products = Product.select()

    buttons = []
    for product in products:
        text += f"{product.name} - {product.price}р.\n"
        buttons.append(InlineKeyboardButton(product.name, callback_data=f'@add_product@{product.id}'))

    footer_keyboard = [
        InlineKeyboardButton('Завершить', callback_data='@doneproducts'),
    ]

    context.user_data['state'] = 1

    reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=2, footer_buttons=footer_keyboard))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=reply_markup)

    return 0


def address(update, context):
    query = update.callback_query
    query.edit_message_text(text=query.message.text, reply_markup=None)

    text = 'Укажите адрес'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    context.user_data['state'] = 2
    return 1


def phone(update, context):
    text = 'Укажите телефон'

    context.user_data['address'] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    context.user_data['state'] = 3

    return 2


def finish_order(update, context):
    context.user_data['phone'] = update.message.text

    order = Order(
        user=User.get(id=update.message.from_user.id),
        products=','.join(context.user_data['products']),
        address=context.user_data['address'],
        phone=context.user_data['phone'],
    )

    order.save()

    text = get_order(order)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    admins = User.select().where(User.status == 'admin')
    for admin in admins:
        context.bot.send_message(
            chat_id=admin.id,
            text=f"<b>Поступил новый заказ!</b>\n" + get_order(order),
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=get_order_buttons(order)
        )

    context.user_data.clear()

    return ConversationHandler.END


@checkuser
def my_orders(update, context):
    user = User.get(id=update.message.from_user.id)
    if user.orders:
        text = "<b>Ваши заказы:</b>\n"
        orders = get_user_orders(user)
        text += orders.text
        reply_markup = orders.reply_markup
    else:
        text = "У вас еще нет заказов."
        reply_markup = None

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup
    )
