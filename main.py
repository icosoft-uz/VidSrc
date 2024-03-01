import asyncio
import logging
import sys

from db.database import Search
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

bot = Bot(token=cfg.bot_token)
dp = Dispatcher(storage=MemoryStorage())
router = Router(name='Main')
db = Search()


class Search(StatesGroup):
    title = State()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Hello! I'm ready to assist you. ✨\nWhat would you like to do?",
                         reply_markup=inline.main())


@dp.message(Command('search'))
async def search(message: Message, state: FSMContext):
    await message.answer("Enter the title of movie:",
                         reply_markup=inline.back())
    await state.set_state(Search.title)


@dp.message(Search.title)
async def search(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    title = data.get('title')
    movie = db.search(query=title, result_type=1)
    tv = db.search(query=title, result_type=2)
    await message.answer(f"Movies:\n{movie}\n\nTV:\n{tv}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(dp.start_polling(bot))
