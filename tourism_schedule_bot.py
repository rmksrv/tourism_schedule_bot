from telegram.ext import Updater, CallbackContext, Filters, MessageHandler

from core.handlers import message_handler, command_handler


def main():
    print("Start")
    updater = Updater(
        token=r"5157680259:AAGmL2XMDVxShr3R7IVtkEbRrwHZStYmy7s",
        use_context=True,
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.command, callback=command_handler))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
