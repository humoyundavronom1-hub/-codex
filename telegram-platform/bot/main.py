import logging
import os
from dotenv import load_dotenv
import telebot
from bot.config import BOT_TOKEN
from bot.storage.db import SessionLocal, init_db
from bot.handlers.member_handlers import register_member_handlers
from bot.handlers.command_handlers import register_command_handlers
from bot.handlers.message_handlers import register_message_handlers

load_dotenv()
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO))
logger = logging.getLogger('bot')

if not BOT_TOKEN:
    raise RuntimeError('BOT_TOKEN belgilanmagan')

init_db()
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')
register_member_handlers(bot, SessionLocal)
register_command_handlers(bot, SessionLocal)
register_message_handlers(bot, SessionLocal)

if __name__ == '__main__':
    logger.info('Bot ishga tushdi')
    bot.infinity_polling(skip_pending=True)
