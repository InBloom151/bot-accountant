import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import API_TOKEN, ALLOWED_USERS, buttons
from db import init_db, get_connection

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class IsAllowedUser(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ALLOWED_USERS

keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

class MeterStates(StatesGroup):
    water_meter = State()
    electricity_meter = State()

class CostStates(StatesGroup):
    water_cost = State()
    electricity_cost = State()

class CalculateStates(StatesGroup):
    new_water_meter = State()
    new_electricity_meter = State()

@dp.message(Command('start'), IsAllowedUser())
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())