from models import *


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


def get_profile(user):
    if user:
        text = f"<b>Профиль</b>\nId - {user.id}\nИмя - {user.name}"
        return text
