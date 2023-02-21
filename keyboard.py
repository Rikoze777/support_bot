from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater, MessageHandler, Filters)


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Заказ", callback_data='1'),
            InlineKeyboardButton("Поддержка", callback_data='2'),
        ],
        [InlineKeyboardButton("Контакты", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Пожалуйста, сделайте выбор:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
