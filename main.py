import asyncio
import logging
import sys
from buttons import inline, default
import config as cfg
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    web_app_info,
    ReplyKeyboardRemove,
    Message,
    CallbackQuery)

bot = Bot(token=cfg.bot_token, protect_content=True, parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())
router = Router(name='Main')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
