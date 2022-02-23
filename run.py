from pathlib import Path

from aiogram import executor
from loguru import logger

from core.bot import dispatcher, redis_url
from core.handlers import register_handlers
from services.schedule_service import ScheduleService


def setup_logger(file: Path) -> None:
    logger.add(file, format="{time} {level} {message}", level="DEBUG")


async def on_startup(_):
    setup_logger(Path("debug.log"))

    logger.info("Starting up!")
    logger.debug(f"Redis url: {redis_url}")
    register_handlers(dispatcher)
    # Init services first time
    ScheduleService()
    logger.info("Bot is online!")


async def on_shutdown(_):
    logger.info("Shutting down!")
    logger.info("Closing storage")
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info("Bot is offline!")


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
