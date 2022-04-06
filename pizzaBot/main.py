import logging

from telegram import Bot
from telegram.ext import Updater

from command_handler import command_handler


TOKEN = '5153387425:AAHY4iARr7AoDhyXkctO85PFKSEjQBpWOk4'


def main():
    bot = Bot(token=TOKEN)


    print(bot)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    command_handler(dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
