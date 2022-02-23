import os
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

bot_token = os.environ.get("TOURISM_SCHEDULE_BOT_TOKEN")
redis_url = os.environ.get("REDIS_URL")


if not bot_token:
    logger.error('No bot token defined! Please, pass it to "TOURISM_SCHEDULE_BOT_TOKEN" env var. Closing...')
    exit()


if not redis_url:
    logger.error('No redis url defined! Please, pass it to "REDIS_URL" env var. Closing...')
    exit()

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
redis_url = urlparse(redis_url)
dispatcher = Dispatcher(bot, storage=RedisStorage2(redis_url.hostname, redis_url.port, password=redis_url.password))
