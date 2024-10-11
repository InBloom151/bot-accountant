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

keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=button)] for button in buttons],
    resize_keyboard=True
)

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

''' SET UNITS '''

@dp.message(F.text == buttons[0], IsAllowedUser())
async def cmd_start_meter_input(message: types.Message, state: FSMContext):
    await state.set_state(MeterStates.water_meter)
    await message.answer("Введите текущее значение счетчика воды:")

@dp.message(MeterStates.water_meter, IsAllowedUser())
async def process_water_meter(message: types.Message, state: FSMContext):
    try:
        water_meter = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    await state.update_data(water_meter=water_meter)
    await state.set_state(MeterStates.electricity_meter)
    await message.answer("Введите текущее значение счетчика электроэнергии:")

@dp.message(MeterStates.electricity_meter, IsAllowedUser())
async def process_electricity_meter(message: types.Message, state: FSMContext):
    try:
        electricity_meter = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    data = await state.get_data()
    water_meter = data.get('water_meter')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO meters (user_id, water_meter, electricity_meter)
        VALUES (?, ?, ?)
    ''', (message.from_user.id, water_meter, electricity_meter))
    conn.commit()
    conn.close()

    await message.answer("Показания счетчиков сохранены.", reply_markup=keyboard)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())