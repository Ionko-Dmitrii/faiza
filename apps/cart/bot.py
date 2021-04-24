import telebot

from django.conf import settings

from telebot.apihelper import ApiException
from loguru import logger


bot = telebot.TeleBot('1735545569:AAECVwDK4XwW6NsX2r6vHeV_6fe3dNaZiTk')


def send_telegram_notification(message, chat_id):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except ApiException as exc:
        logger.warning(f'Telegram API exception: {exc}')
