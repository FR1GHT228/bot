from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import Database

role = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🧠Психолог'),
                                      KeyboardButton(text='🤔Клиент')]],
                           resize_keyboard=True, )

psy_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📋Правила'),
                                              KeyboardButton(text='📞Связаться с менеджером')],
                                             [KeyboardButton(text='🎓Курсы'),
                                              KeyboardButton(text='👥Клиенты')]],
                                   resize_keyboard=True,
                                   input_field_placeholder='Выберите пункт меню...')

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='🌐Сменить язык'),
                                      KeyboardButton(text='🤖ИИ психолог')],
                                     [KeyboardButton(text='📞Связаться с менеджером'),
                                      KeyboardButton(text='📋Правила')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

language = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Русский', callback_data='russian')],
    [InlineKeyboardButton(text='Узбекский', callback_data='uzbek')],
    [InlineKeyboardButton(text='Английский', callback_data='english')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='☎️Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True)

continue_btn = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📝Заполнить анкету')]],
                                   resize_keyboard=True)

continue_btn_client = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📝Заполнить заявку')]],
                                   resize_keyboard=True)

approve_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить заявку', callback_data='approve')]
])

course_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Старт в психологии', callback_data='psychology_start', url='https://t.me/+fVJICNKJb_k3NDMy')]
])

manager_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Связаться с менеджером', callback_data='manager_connect', url='')]
])

genders = ['Мужской', 'Женский']

async def inline_gender():
    keyboard = ReplyKeyboardBuilder()
    for gender in genders:
        keyboard.add(KeyboardButton(text=gender))
    return keyboard.adjust(2).as_markup()


choices = ['Да', 'Нет']


async def inline_choice():
    keyboard = ReplyKeyboardBuilder()
    for choice in choices:
        keyboard.add(KeyboardButton(text=choice))
    return keyboard.adjust(2).as_markup()


psy_genders = ['Мужчина', 'Женщина', 'Неважно']


async def inline_psyGender():
    keyboard = ReplyKeyboardBuilder()
    for psy_gender in psy_genders:
        keyboard.add(KeyboardButton(text=psy_gender))
    return keyboard.adjust(2).as_markup()


graduations = ['Высшее образование', 'Среднее специальное', 'Прохождение курсов переподготовки с сертификатом',
               'Еще учусь', 'Профильное медицинское (имеете ли вы прово выписывать медикаменты)']


async def inline_graduation():
    keyboard = ReplyKeyboardBuilder()
    for graduation in graduations:
        keyboard.add(KeyboardButton(text=graduation))
    return keyboard.adjust(3).as_markup()


howFinds = ['Соц.сети', 'Знакомые рассказали', 'Реклама(листовки)']


async def inline_howFind():
    keyboard = ReplyKeyboardBuilder()
    for howFind in howFinds:
        keyboard.add(KeyboardButton(text=howFind))
    return keyboard.adjust(1).as_markup()


languages = ['Русский', 'Узбекский']


async def inline_language():
    keyboard = ReplyKeyboardBuilder()
    for language in languages:
        keyboard.add(KeyboardButton(text=language))
    return keyboard.adjust(1).as_markup()

async def clients():
    all_clients = await Database.get_user()
    keyboard = InlineKeyboardBuilder
    for client in all_clients:
        keyboard.add(InlineKeyboardButton(text=psy.name, callback_data=f'client_{client.id}'))
    return keyboard.adjust(1).as_markup()
