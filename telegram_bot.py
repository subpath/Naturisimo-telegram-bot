# global
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# project
from manage_db import DataHandler
from bot_messages import START_MESSAGE, STOP_MESSAGE, INFO_MESSAGE
from config import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    db = DataHandler()
    db.connect()
    db.create_table('users', 'chat_id')
    db.check_updates('users', str(update.message.chat_id))
    update.message.reply_text(START_MESSAGE)
    db.close_connection()


def stop(bot, update):
    """Send a message when the command /start is issued."""
    db = DataHandler()
    db.connect()
    db.delete_user('users', str(update.message.chat_id))
    update.message.reply_text(STOP_MESSAGE)
    db.close_connection()


def info(bot, update):
    """Send a message when the command /info is issued."""
    db = DataHandler()
    db.connect()
    db.close_connection()
    update.message.reply_text(INFO_MESSAGE)


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
