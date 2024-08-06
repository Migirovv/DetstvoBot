from aiogram import F, Router, Bot, types
from aiogram.enums import ChatAction
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboard as kb

TOKEN = '6528747103:AAHDX2EZk2fe_rZeRPuFVgPb1sjtEoQPKHc'
bot = Bot(TOKEN)


router = Router()


class Register(StatesGroup):
    age = State()
    sex = State()
    name = State()
    number = State()
    is_agree = State()


# Start command handler
@router.message(CommandStart())
async def hello(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING)
    await message.reply(f"Здравстуйте, {message.chat.first_name}!\nДобро пожаловать в наш чат бот!"
                        f" Здесь вы сможете узнать больше о нашем ансамбле,"
                        f" а также оставить заявку\n"
                        "Хотите ли Вы посетить наш веб-сайт?",
                        reply_markup=kb.main)


# Web site handler
@router.message(F.text == 'Веб-сайт')
async def web(message: Message):
    await message.answer('https://лучшеедетство.рф')


# Request handler
@router.message(F.text == 'Оставить заявку')
async def web(message: Message):
    file_path = './Screenshot/Detstvo.png'
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING)
    await message.reply_photo(
        photo=types.FSInputFile(file_path),
        caption="На нашем сайте есть копка <b>Бесплатное пробное занятие</b>.\n"
                "Заполните форму, и мы вскоре с Вами свяжемся!", parse_mode='html')
    await message.answer('https://лучшеедетство.рф')


# info handler
@router.message(F.text == 'Выбрать группу для ребенка')
async def web(message: Message, state: FSMContext):
    await message.answer('Укажите пол ребенка', reply_markup=kb.sex)
    await state.set_state(Register.sex)


# info - boy handler
@router.callback_query(F.data == 'Мальчик')
async def web(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback.data)
    data = await state.get_data()
    await callback.answer(f"Ваш выбор - {data['sex']}", show_alert=True)
    await callback.message.answer('Укажите возраст ребенка')
    await state.set_state(Register.age)


# info - girl handler
@router.callback_query(F.data == 'Девочка')
async def web(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback.data)
    data = await state.get_data()
    await callback.answer(f"Ваш выбор - {data['sex']}", show_alert=True)
    await callback.message.answer('Укажите возраст ребенка')
    await state.set_state(Register.age)


# age handler
@router.message(Register.age)
async def web(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.reply('Простите, я всего лишь бот(компьютерная программа), а не разумный человек.'
                            ' В данный момент я могу распознать только числовое значение,'
                            ' обозначающее возраст только одного ребенка.'
                            ' Пожалуйста, введите возраст одним числом и без иных символов \U0001F604')
        return
    await state.update_data(age=age)
    if age < 4:
        await message.reply('На данный момент младшая группа от 4 лет')
    elif 4 <= age <= 6:
        await message.reply('Ведется набор группу 4 - 6 лет.')
    elif 7 <= age <= 9:
        await message.reply('Есть группа 7 - 9 лет.')
    elif 10 <= age <= 14:
        await message.reply('Есть группа 10 - 14 лет.')
    else:
        await message.reply("На данный момент старшая группа до 14 лет включительно. Пожалуйста, заполните форму"
                            ", и мы скоро с Вами свяжемся")
    await message.answer("Хотите оставить свои данные?")
    await state.set_state(Register.is_agree)


# leave personal info handler
@router.message(Register.is_agree)
async def web(message: Message, state: FSMContext):
    answer = message.text
    if answer.lower() == 'да':
        await state.set_state(Register.name)
        await message.answer('Как Вас зовут?')
    else:
        await state.clear()
        await message.reply('Хорошо, всю информацию, а также ссылку на форму,'
                            ' можно найти на нашем сайте.')
        await message.answer('https://лучшеедетство.рф')


# personal - name handler
@router.message(Register.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.number)
    await message.answer("Введите номер телефона")


# personal - number handler
@router.message(Register.number)
async def web(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=646104355,
                           text=f'Имя родителя:{data["name"]}\n'
                                f'Пол ребенка:{data["sex"]}\n'
                                f'Возраст ребенкаЖ:{data["age"]}\n'
                                f'Номер телефона:{data["number"]}')
    await message.answer('Спасибо, мы скоро с Вами свяжемся. Посетите наш сайт!')
    await message.answer('https://лучшеедетство.рф')
    await state.clear()


# Visit our website No
@router.message(F.text.lower() == 'нет')
async def web(message: Message, state: FSMContext):
    await message.answer('Укажите пол ребенка', reply_markup=kb.sex)
    await state.set_state(Register.sex)


# Visit our website Yes
@router.message(F.text.lower() == 'да')
async def web(message: Message):
    await message.answer('https://лучшеедетство.рф')


# Every other input handler
@router.message()
async def web(message: Message):
    answer = message.text.lower()
    greetings = ('привет', 'здравствуй','здравствуйте','добрый','доброе')
    if answer.startswith('спасибо'):
        await message.answer('Всегда рад помочь!')
    else:
        for greeting in greetings:
            if answer.startswith(greeting):
                await message.answer('Здравствуйте! Чем я могу помочь?\n'
                                     '(Выберите подходящий запрос)', reply_markup=kb.main)
                return

    await message.answer("Подробная информация об оплате, местоположении и педагогах"
                         " есть на нашем сайте\nhttps://лучшеедетство.рф",
                         reply_markup=kb.main)
