import os
import asyncio
import aiomysql
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.requests import Database

import app.keyboards as kb



PSYCHANNEL_ID = '-4517186238'
CHANNEL_ID = '-4532864138'
BOT_ID = '7439964712'
bot = os.getenv('TOKEN_ID')

#MAX_FILE_SIZE = 50 * 1024 * 1024  # 50мб

router = Router()

loop = asyncio.get_event_loop()

class Register(StatesGroup):
    name = State()
    age = State()
    gender = State()
    diseases = State()
    psy_gender = State()
    first_time = State()
    info = State()
    issue = State()
    experience = State()
    number = State()


class RegisterPsy(StatesGroup):
    psy_name = State()
    psy_age = State()
    psy_gender = State()
    psy_graduation = State()
    psy_language = State()
    psy_how_find = State()
    psy_info = State()
    psy_how_work = State()
    psy_diploma = State()
    psy_number = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Здравствуйте. Выберите вашу роль', reply_markup=kb.role)


# Смена языка
@router.message(F.text == '🌐Сменить язык')
async def language(message: Message):
    await message.answer('Выберите язык:', reply_markup=kb.language)


@router.callback_query(F.data == 'russian')
async def russian(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Вы сменили язык')


# Панель психолога

@router.message(F.text == '🧠Психолог')
async def register(message: Message):
    db = Database()
    if not await db.get_psy(message.from_user.id):
        await message.answer(
            f'Становясь нашим психологом вы подтверждаете условия согласия\nДля того, чтобы продолжить вам нужно заполнить анкету\n\nПолитика конфидециальности:\nhttps://telegra.ph/Politika-v-otnoshenii-obrabotki-personalnyh-dannyh-09-06-6\n\nПубличная офера:\nhttps://telegra.ph/PUBLICHNAYA-OFERTA-09-06-2')
        await message.answer('Продолжить?', reply_markup=kb.continue_btn)
    else:
        await message.answer('Вы уже зарегистрированны', reply_markup=kb.psy_keyboard)


# Регистрация психолога

@router.message(F.text == '📝Заполнить анкету')
async def register_psy(message: Message, state: FSMContext):
    await state.set_state(RegisterPsy.psy_name)
    await message.answer('Введите ФИО', reply_markup=ReplyKeyboardRemove())


@router.message(RegisterPsy.psy_name)
async def register_psy_name(message: Message, state: FSMContext):
    await state.update_data(psy_name=message.text)
    await state.set_state(RegisterPsy.psy_age)
    await message.answer('Введите ваш возраст')


@router.message(RegisterPsy.psy_age)
async def register_psy_age(message: Message, state: FSMContext):
    await state.update_data(psy_age=message.text)
    await state.set_state(RegisterPsy.psy_gender)
    await message.answer('Введите ваш пол', reply_markup=await kb.inline_gender())


@router.message(RegisterPsy.psy_gender)
async def register_psy_gender(message: Message, state: FSMContext):
    await state.update_data(psy_gender=message.text)
    await state.set_state(RegisterPsy.psy_graduation)
    await message.answer('Какое есть психологическое образование?(Можно написать свой вариант)',
                         reply_markup=await kb.inline_graduation())


@router.message(RegisterPsy.psy_graduation)
async def register_psy_graduation(message: Message, state: FSMContext):
    await state.update_data(psy_graduation=message.text)
    await state.set_state(RegisterPsy.psy_language)
    await message.answer('На каких языках можете консультировать?', reply_markup=await kb.inline_language())


@router.message(RegisterPsy.psy_language)
async def register_pay_language(message: Message, state: FSMContext):
    await state.update_data(psy_language=message.text)
    await state.set_state(RegisterPsy.psy_how_find)
    await message.answer('Как вы о нас узнали?(Можно написать свой вариант)', reply_markup=await kb.inline_howFind())


@router.message(RegisterPsy.psy_how_find)
async def register_psy_how_find(message: Message, state: FSMContext):
    await state.update_data(psy_how_find=message.text)
    await state.set_state(RegisterPsy.psy_info)
    await message.answer('Кратко о себе', reply_markup=ReplyKeyboardRemove())


@router.message(RegisterPsy.psy_info)
async def register_psy_info(message: Message, state: FSMContext):
    await state.update_data(psy_info=message.text)
    await state.set_state(RegisterPsy.psy_how_work)
    await message.answer('Каким основным психологическим инструментом/подходом пользуетесь?')


@router.message(RegisterPsy.psy_how_work)
async def register_psy_how_work(message: Message, state: FSMContext):
    await state.update_data(psy_how_work=message.text)
    await state.set_state(RegisterPsy.psy_diploma)
    await message.answer('Прикрепите документ об образовании или студенческий билет')


@router.message(RegisterPsy.psy_diploma)
async def register_psy_diploma(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    await state.update_data(psy_diploma=file_id)
    await message.bot.send_photo(chat_id=os.getenv('PSYCHANNEL_ID'), photo=file_id)
    await state.set_state(RegisterPsy.psy_number)
    await message.answer('Отправте номер телефона', reply_markup=kb.get_number)

@router.message(RegisterPsy.psy_number)
async def register_psy_number(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(psy_number=message.contact.phone_number)
    db = Database()
    data = await state.get_data()
    await bot.send_message(chat_id=PSYCHANNEL_ID,
                           text=f'Имя: {data["psy_name"]}\nВозраст: {data["psy_age"]}\n'
                                f'Номер телефона: {data["psy_number"]}\nПол: {data["psy_gender"]}\n'
                                f'Образование: {data["psy_graduation"]}\nЯзык: {data["psy_language"]}\n'
                                f' психологе: {data["psy_info"]}\nКак узнали: {data["psy_how_find"]}\n'
                                f'Метод работы: {data["psy_how_work"]}',
                                reply_markup=kb.approve_button)
    await db.add_psy(message.from_user.id, data['psy_name'], data['psy_age'], data['psy_gender'],
                     data['psy_graduation'], data['psy_language'], data['psy_how_find'],
                     data['psy_info'], data['psy_how_work'], data['psy_number'])
    await state.clear()
    await message.answer('Ваша заявка на рассмотрении', reply_markup=ReplyKeyboardRemove())


# Одобрение заявки психолога

# @router.message(F.text == 'Благодорим за вашу заявку, скоро с вами свяжутся')
# async def notify_admin(message: Message, state: FSMContext):
#    await state.update_data(user_message=message.text)
#    await bot.send_message(PSYCHANNEL_ID, 'Одобрить заявку',reply_markup=kb.approve_button)

# @router.callback_query(F.data == 'approve')
# async def processed_button_press(callback_query: CallbackQuery):
#    await callback_query.answer('Доступ одобрен')

#Курсы

@router.message(F.text == '🎓Курсы')
async def courses(message: Message):
    await message.answer('Курсы', reply_markup=kb.course_btn)

#Вывод клиентов
async def connect_to_db():
    conn = await aiomysql.connect(host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USER'),
                           password=os.getenv('DB_PASSWORD'),
                           db=os.getenv('DB_NAME'),
                           loop=loop)
    return conn

async def get_db_data():
    conn = await connect_to_db()
    cur = await conn.cursor()
    await cur.execute("SELECT id, tg_id, name, age, gender, diseases, psy_gender,"
                      " first_time, info, issue, experience, number FROM users WHERE approve = 0")
    result = await cur.fetchall()
    await cur.close()
    conn.close()
    return result

@router.message(F.text == '👥Клиенты')
async def show_clients(message: Message):
    db_data = await get_db_data()
    for row in db_data:
        id, tg_id, name, age, gender, diseases, psy_gender, first_time, info, issue, experience, number = row

        await message.answer(f'id: {id}\ntg_id: {tg_id}\nname: {name}\nage: {age}\ngender: {gender}\n'
                             f'diseases: {diseases}\npsy_gender: {psy_gender}\nПервый раз: {first_time}\n'
                             f'Информация: {info}\nПричина: {issue}\nОпыт: {experience}\n'
                             f'Номер телефона: {number}', reply_markup=kb.approve_button)






#Связаться с менеджером

@router.message(F.text == '📞Связаться с менеджером')
async def courses(message: Message):
    await message.answer('Вы хотите связаться с менеджером?', reply_markup=kb.manager_btn)

# Меню клиента

@router.message(F.text == '🤔Клиент')
async def client(message: Message, state: FSMContext):
    db = Database()
    if not await db.get_user(message.from_user.id):
        await message.answer('Пожалуйста заполните анкету.\n\n'
                             'Старайтесь отвечать открыто, полноценно и честно. После прохождения анкеты с вами свяжутся в Telegramm для последующей связи. Все ваши ответы строго конфиденциальны и используются только для того, чтобы подобрать наиболее подходящего вам специалиста для оказания грамотных услуг')
        await message.answer('Продолжить?', reply_markup=kb.continue_btn_client)
    else:
        await message.answer('Вы уже зарегистрированны', reply_markup=kb.main)


@router.message(F.text == '📋Правила')
async def rules(message: Message):
    await message.answer('Условия для клиентов проекта «Доступная психология>\n'
                         '1. Стоимость консультаций:\n- 50000 сум за одну сессию.\n'
                         '2. Количество сессий:\n- Обязательно пройти 10 сессий.\n'
                         '3. Организационный взнос: \n- 50000 сум (невозвратный).\n'
                         '4. Условия участия:\n - Готовность пройти 10 сессий с начинающим психологом.\n'
                         '- Приоритет отдается клиентам, готовым оплатить все 10 сессий сразу.\n - Возможна замена психолога после первой консультации.\n'
                         '5. Продолжительность консультаций:\n - 50-60 минут каждая сессия.\n'
                         '6. Формат сессий:\n - Сессии проходят онлайн.')


@router.message(F.text == '🤖ИИ психолог')
async def rules(message: Message):
    await message.answer('ИИ психолог сейчас в разработке')


# Регистрация клиента

@router.message(F.text == '📝Заполнить заявку')
async def register_psy(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ФИО', reply_markup=ReplyKeyboardRemove())


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.gender)
    await message.answer('Введите ваш пол', reply_markup=await kb.inline_gender())


@router.message(Register.gender)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Register.diseases)
    await message.answer(
        'Есть ли у вас диагностированные психо-неврологические заболевания?(Можно написать свой вариант)',
        reply_markup=await kb.inline_choice())


@router.message(Register.diseases)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(diseases=message.text)
    await state.set_state(Register.psy_gender)
    await message.answer('Предпочтительный пол специалиста', reply_markup=await kb.inline_psyGender())


@router.message(Register.psy_gender)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(psy_gender=message.text)
    await state.set_state(Register.first_time)
    await message.answer('Пользовались ли вы ранее услугами психолога?', reply_markup=await kb.inline_choice())


@router.message(Register.first_time)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(first_time=message.text)
    await state.set_state(Register.info)
    await message.answer(
        'Кратко о себе (семейное положение, наличие детей, род деятельности, как проводите свободное время)',
        reply_markup=ReplyKeyboardRemove())


@router.message(Register.info)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(info=message.text)
    await state.set_state(Register.issue)
    await message.answer('Основная суть запроса/проблемы')


@router.message(Register.issue)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(issue=message.text)
    await state.set_state(Register.experience)
    await message.answer('Если пользовались, то какой опыт вы получили')


@router.message(Register.experience)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)


@router.message(Register.number, F.contact)
async def register_number(message: Message, bot: Bot, state: FSMContext):
    db = Database()
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer('Благодорим за вашу заявку, скоро с вами свяжутся\n\n'
                         '*Если вы оставили неккоректные контактные данные и психолог не может выйти с вами на связь в течении 3х суток, ваша заявка анулируется и организационный взнос не возвращается\n'
                         '*Анкета обрабатывается в течении реального времени и живой очереди, если вы заполнили анкету, то ожидайте связи со специалистом\n'
                         '*При агрессии и оскорблении участника проекта/специалиста вы отправляетесь в бан')
    await bot.send_message(chat_id=CHANNEL_ID,
                           text=f'Имя: {data["name"]}\nВозраст: {data["age"]}\nНомер телефона: {data["number"]}\nПол: {data["gender"]}\nЗаболевания: {data["diseases"]}\nПол психолога: {data["psy_gender"]}\nПервый раз?: {data["first_time"]}\nО клиенте: {data["info"]}\nПроблема: {data["issue"]}\nОпыт: {data["experience"]}')
    await db.add_user(message.from_user.id, data['name'], data['age'], data['gender'],
                      data['diseases'], data['psy_gender'], data['first_time'],
                      data['info'], data['issue'], data['experience'], data['number'])
    await state.clear()


