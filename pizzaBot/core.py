from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from models import *
from menus import *


def is_user_exist(id):
    try:
        user = User.get(id=id)
        if not user.id:
            raise DoesNotExist
        return True
    except DoesNotExist:
        return False


def checkuser(function):
    def check(update, context):
        if not is_user_exist(id=update.message.from_user.id):
            if update.message.from_user.username:
                username = update.message.from_user.username
            else:
                username = 'none'

            user = User.create(
                id=update.message.from_user.id,
                status='user',
                name=update.message.from_user.first_name,
                username=username
            )
            user.save()
        function(update, context)
    return check


def checkadmin(function):
    def check(update, context):
        user = User.get(id=update.message.from_user.id)
        if user.status == 'admin':
            function(update, context)
    return check


def get_profile(user):
    if user:
        text = f"<b>Профиль</b>\n" \
               f"Id: <code>{user.id}</code>\n" \
               f"Статус: {user.status}\n" \
               f"Имя: {user.name}\n" \
               f"@{user.username}"
        return text


def get_user_buttons(user):
    if user:
        buttons =[InlineKeyboardButton('Заказы', callback_data=f"@userorders@{user.id}")]
        return InlineKeyboardMarkup(build_menu(buttons, n_cols=1))


def get_user_orders(user, admin=False):
    buttons = []
    text = ''
    prefix = ''
    if admin:
        prefix = 'admin'
    for order in user.orders:
        text += f"Заказ #<code>{order.id}</code>\n"
        buttons.append(InlineKeyboardButton(f"Заказ {order.id}", callback_data=f'@{prefix}order@{order.id}'))
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))

    user_orders = namedtuple('menu', 'text reply_markup')
    user_orders.text = text
    user_orders.reply_markup = reply_markup
    return user_orders


def get_order(order, user=False):
    if order:
        text = ''
        if user:
            user = User.get(id=order.user)
            text += f"Пользователь #<code>{user.id}</code> @{user.username}\n"

        text += f"<b>Заказ #{order.id}</b>\n\n"\
                f"Статус: <i>{order.status}</i>\n"\
                f"Адрес: <i>{order.address}</i>\n"\
                f"Телефон: <i>{order.phone}</i>\n\n"

        prod_text = f"Состав:\n"
        total = 0
        for product_id in order.products.split(','):
            product = Product.get(id=product_id)
            prod_text += f"\t\t\t\t\t\t<i>{product.name} - {product.price}р.</i>\n"
            total += product.price
        prod_text += f"\n\t\t\t\t\t\t<i>Всего: {total}р.</i>"

        text += prod_text

        return text


def get_order_buttons(order):
    buttons = []

    if order.status == 'В обработке':
        buttons.append(InlineKeyboardButton('Подтвердить заказ', callback_data=f"@confirm@{order.id}"))
    if order.status == 'Принят':
        buttons.append(InlineKeyboardButton('Завершить заказ', callback_data=f"@complete@{order.id}"))
    buttons.append(InlineKeyboardButton('Удалить заказ', callback_data=f"@delete@{order.id}"))
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=1))