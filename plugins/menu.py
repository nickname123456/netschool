from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from netschoolapi import NetSchoolAPI
from sqlighter import SQLighter
import logging


bp = Blueprint('menu')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр

db = SQLighter('database.db')# Подключаемся к базеданных



#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.private_message(text=["Меню"])
@bp.on.private_message(payload={'cmd': 'menu'})
async def menu(message: Message):
    logging.info(f'{message.peer_id}: I get menu')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    try:
        api = NetSchoolAPI(db.get_account_link(user_id))
        await api.login(
            db.get_account_login(user_id), 
            db.get_account_password(user_id), 
            db.get_account_school(user_id)
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!\n Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    settings = await api.userInfo()
    name = settings['Имя']

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Войти', {'cmd': 'login'}), color=KeyboardButtonColor.POSITIVE)
        #Начать с новой строки
        .row()
        .add(Text('Дневник', {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Домашнее задание', {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Объявления', {'cmd': 'announcements'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Оценки', {'cmd': ' '}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('🔁', {'cmd': 'start'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'{name}', {'cmd': 'information'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⚙', {'cmd': 'keyboard_settings'}), color=KeyboardButtonColor.SECONDARY)
    )

    #Ответ в чат
    await message.answer('Ты в главном меню.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent menu')







#Если написали "Меню" или нажали на соответствующую кнопку
@bp.on.chat_message(text=["Меню"])
@bp.on.chat_message(payload={'cmd': 'menu'})
async def menu(message: Message):
    logging.info(f'{message.peer_id}: I get menu')
    # Айди чата:
    chat_id = message.chat_id

    try:
        api = NetSchoolAPI(db.get_chat_link(chat_id))
        await api.login(
            db.get_chat_login(chat_id), 
            db.get_chat_password(chat_id), 
            db.get_chat_school(chat_id)
        )
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!\n Настоятельно рекомендую написать "Начать", для повторной регистрации')
        return

    settings = await api.userInfo()
    name = settings['Имя']

    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопки
        .add(Text('Войти', {'cmd': 'login'}), color=KeyboardButtonColor.POSITIVE)
        #Начать с новой строки
        .row()
        .add(Text('Дневник', {'cmd': 'keyboard_diary'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Домашнее задание', {'cmd': 'keyboard_homework'}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('Расписание', {'cmd': 'keyboard_schedule'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Объявления', {'cmd': 'announcements'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text('Оценки', {'cmd': ' '}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text('🔁', {'cmd': 'not_found'}), color=KeyboardButtonColor.SECONDARY)
        .add(Text(f'{name}', {'cmd': 'information'}), color=KeyboardButtonColor.PRIMARY)
        .add(Text('⚙', {'cmd': 'keyboard_settings'}), color=KeyboardButtonColor.SECONDARY)
    )

    #Ответ в чат
    await message.answer('Ты в главном меню.', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent menu')