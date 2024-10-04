from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = '7599027775:AAGSRofHLSpF4VTn3NE43q-ggsPxcYYMPSs'  # получили в ТГ от BotFather
bot = Bot(token=api)  # переменная бота - она будет хранить объект бота, 'token' будет равен вписанному ключу в 'api'
dp = Dispatcher(bot, storage=MemoryStorage())  # создадим объект 'Dispatcher' и наш объект бота в качестве аргумента


class UserState(StatesGroup):
    """age: возраст, growth: рост, weight: вес"""
    age = State()
    growth = State()
    weight = State()


# Создали клавиатуру в переменной 'kb', создали и добавили две кнопки в одной строке,
# указали параметр для подстраивания клавиатуры под размеры интерфейса устройства
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
                                   [KeyboardButton(text='Купить')]],
                         resize_keyboard=True)

# Создали внутреннюю клавиатуру с двумя кнопками в одной строке
in_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
     InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
])

# Создали внутреннюю клавиатуру с кнопками выбора продукта
in_kb_product = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Продукт1', callback_data='product_buying'),
                      InlineKeyboardButton(text='Продукт2', callback_data='product_buying'),
                      InlineKeyboardButton(text='Продукт3', callback_data='product_buying'),
                      InlineKeyboardButton(text='Продукт4', callback_data='product_buying')]])


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)  # добавили параметр reply_markup


@dp.message_handler(text='Купить')
async def get_buying_list(message):    # отображение кнопок с картиками для выбора продукта
    for i in range(1, 5):
        with open(f'files/{i}.png', 'rb') as img:
            await message.answer(f'Название: Product{i} | Описание: описание{i} | Цена: {i * 100}')
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=in_kb_product)


@dp.callback_query_handler(text='product_buying')    # обработчик внутренних кнопок 'Продукт'
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)


@dp.callback_query_handler(text='formulas')    # обработчик внутренней кнопки 'Формулы расчёта'
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


@dp.callback_query_handler(text='calories')    # обработчик внутренней кнопки 'Рассчитать норму калорий'
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()    # ожидаем ввода возраста в атрибут 'UserState.age'


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)    # эта функция обновляет данные в состоянии age на message.text
    await message.answer('Введите свой рост:')
    await UserState.growth.set()    # ожидаем ввода роста в атрибут 'UserState.growth'


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)    # эта функция обновляет данные в состоянии growth на message.text
    await message.answer('Введите свой вес:')
    await UserState.weight.set()    # ожидаем ввода веса в атрибут 'UserState.weight'


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)    # эта функция обновляет данные в состоянии weight на message.text
    data = await state.get_data()    # запомнили в переменную data все ранее введённые состояния
    # calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161    # для женщин
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5    # для мужчин
    await message.answer(f'Ваша норма калорий {calories} в сутки')
    await state.finish()    # финишировали машину состояний


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # запуск бота
