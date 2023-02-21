import logging
import sys
from time import sleep

import telegram
from environs import Env
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, Update,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
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


AUTHORIZATION, STATUS= range(4)


def authorization(update, context):
    # Список кнопок для ответа
    reply_keyboard = [['Заказчик', 'Работник']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Добрый день, Вас приветствует бот поддержки '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Выберетие Ваш статус',
        reply_markup=markup_key,)
    return AUTHORIZATION


def get_phone(update, context):
    user_info = {}
    user = update.message.text
    user_info["user_id"] = update.message.from_user.id
    user_info["full_name"] = user
    split_name = user.split()
    if not validate_fullname(split_name):
        update.message.reply_text(
            "*Введите корректные имя и фамилию!*\nПример: Василий Петров",
            parse_mode="Markdown"
        )
    if validate_fullname(split_name):
        message_keyboard = [
            [
                KeyboardButton(
                    "Отправить свой номер телефона", request_contact=True
                )
            ]
        ]
        markup = ReplyKeyboardMarkup(
            message_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
        update.message.reply_text(
            f"Введите телефон в формате +7... или нажав на кнопку ниже:", 
            reply_markup=markup
        )
        return GET_PHONE


def start(update, context):
    # Список кнопок для ответа
    reply_keyboard = [['Заказчик', 'Работник']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Добрый день, Вас приветствует бот поддержки '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Выберетие Ваш статус',
        reply_markup=markup_key,)
    return STATUS


def cancel(update, context):
    chat_id = update.effective_chat.id
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=update.message.message_id
    )
    return ConversationHandler.END


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


    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
