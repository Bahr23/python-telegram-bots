def btn_handler(update, context):
    query = update.callback_query
    data = query.data.split("@")[1:]
    if data[0] == 'add_product':
        if 'products' in context.user_data:
            context.user_data['products'].append(data[1])
        else:
            context.user_data['products'] = [data[1]]

        text = f'Вы добавили {data[1]} в заказ.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)