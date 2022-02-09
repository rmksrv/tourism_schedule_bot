import os
from pathlib import Path

from telegram.ext import Updater, CallbackContext, Filters, MessageHandler

from core.handlers import message_handler, command_handler
from core.downloader import schedule_doc_data, download


def main():
    assert os.environ.get("tourism_schedule_bot_token"), "No token provided"

    print("Start")
    print("Download schedule")
    schedule_filename, schedule_doc_link = schedule_doc_data()
    download(schedule_doc_link, Path(".") / schedule_filename)

    updater = Updater(
        token=os.environ["tourism_schedule_bot_token"],
        use_context=True,
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.command, callback=command_handler)
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.text, callback=message_handler)
    )

    print("Polling")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
