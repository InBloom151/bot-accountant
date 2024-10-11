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

init_db()

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

class CurrentMeterStates(StatesGroup):
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

''' SET UTILITIES '''

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
        INSERT INTO meters (water_meter, electricity_meter)
        VALUES (?, ?)
    ''', (water_meter, electricity_meter))
    conn.commit()
    conn.close()

    await message.answer("Показания счетчиков сохранены.", reply_markup=keyboard)
    await state.clear()

''' SET COSTS '''

@dp.message(F.text == buttons[1], IsAllowedUser())
async def cmd_start_cost_input(message: types.Message, state: FSMContext):
    await state.set_state(CostStates.water_cost)
    await message.answer("Введите текущую стоимость воды:")

@dp.message(CostStates.water_cost, IsAllowedUser())
async def process_water_cost(message: types.Message, state: FSMContext):
    try:
        water_cost = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    await state.update_data(water_cost=water_cost)
    await state.set_state(CostStates.electricity_cost)
    await message.answer("Введите текущую стоимость электроэнергии (руб/кВт·ч):")

@dp.message(CostStates.electricity_cost, IsAllowedUser())
async def process_electricity_cost(message: types.Message, state: FSMContext):
    try:
        electricity_cost = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    data = await state.get_data()
    water_cost = data.get('water_cost')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO costs (water_cost, electricity_cost)
        VALUES (?, ?)
    ''', (water_cost, electricity_cost))
    conn.commit()
    conn.close()

    await message.answer("Стоимость ресурсов сохранена.", reply_markup=keyboard)
    await state.clear()

''' SET CURRENT UTILITIES '''

@dp.message(F.text == buttons[2], IsAllowedUser())
async def set_current_meter_input(message: types.Message, state: FSMContext):
    await state.set_state(CurrentMeterStates.water_meter)
    await message.answer("Введите новое значение счетчика воды:")
    await state.update_data(update=True)

@dp.message(CurrentMeterStates.water_meter, IsAllowedUser())
async def process_current_water_meter(message: types.Message, state: FSMContext):
    try:
        water_meter = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    await state.update_data(water_meter=water_meter)
    await state.set_state(CurrentMeterStates.electricity_meter)
    await message.answer("Введите текущее значение счетчика электроэнергии:")

@dp.message(CurrentMeterStates.electricity_meter, IsAllowedUser())
async def process_current_electricity_meter(message: types.Message, state: FSMContext):
    try:
        electricity_meter = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    data = await state.get_data()
    water_meter = data.get('water_meter')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM current_meters WHERE id = 1")
    exists = cursor.fetchone()[0]
    if exists:
        cursor.execute('''
                UPDATE current_meters SET water_meter = ?, electricity_meter = ?
                WHERE id = 1
            ''', (water_meter, electricity_meter))
        await message.answer("Показания счетчиков обновлены.", reply_markup=keyboard)
    else:
        cursor.execute('''
                INSERT INTO current_meters (water_meter, electricity_meter)
                VALUES (?, ?)
            ''', (water_meter, electricity_meter))
        await message.answer("Показания счетчиков сохранены.", reply_markup=keyboard)
    conn.commit()
    conn.close()
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())