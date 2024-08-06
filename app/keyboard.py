from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
# Inline Buttons (callback returned)
catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Option 1', callback_data='1')],
    [InlineKeyboardButton(text='Option 2', callback_data='2'),
     InlineKeyboardButton(text='Option 2.5', callback_data='2.5')],])

# Reply buttons
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Веб-сайт'),
     KeyboardButton(text='Выбрать группу для ребенка')],
    [KeyboardButton(text='Оставить заявку')]
    ],
    resize_keyboard=True, input_field_placeholder='Выберите подходящий вариант...')

sex = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мальчик', callback_data='Мальчик'),
     InlineKeyboardButton(text='Девочка', callback_data='Девочка')],
    ],
    resize_keyboard=True)
