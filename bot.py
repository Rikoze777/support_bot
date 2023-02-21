import logging
import sys
from time import sleep

import telegram
from environs import Env
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater, MessageHandler, Filters)
from keyboard import start, button

logger = logging.getLogger(__name__)


class LogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to use this bot.")


def reply_to_message(update: Update, context: CallbackContext) -> None:
    session_id = f'tg-{update.effective_user.id}'
    try:
        answer = ""
        update.message.reply_text(answer.fulfillment_text)
    except NetworkError as netword_error:
        logger.warning(f'Network error: {netword_error}\n')
        sleep(20)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")
    user_id = env.str('USER_ID')
    bot = telegram.Bot(token=tg_token)
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        filename='bot.log',
        filemode='w',
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.addHandler(LogsHandler(bot, user_id))
    logger.info('Бот запущен')
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text,
                           reply_to_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
