from pathlib import Path

from aiogram import executor
from loguru import logger

from core.bot import dispatcher
from core.handlers import register_handlers
from services.schedule_service import ScheduleService


def setup_logger(file: Path) -> None:
    logger.add(file, format="{time} {level} {message}", level="DEBUG")


async def on_startup(_):
    setup_logger(Path("debug.log"))
    register_handlers(dispatcher)
    ScheduleService()
    logger.info("Bot is online!")


async def on_shutdown(_):
    logger.info("Bot is offline!")


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
