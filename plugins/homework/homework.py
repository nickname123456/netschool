from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
import logging


bp = Blueprint('homework') # Объявляем команду
db = SQLighter('database.db')# Подключаемся к базеданных




@bp.on.private_message(payload={'cmd': 'homework'})
async def keyboard_schedule(message: Message):
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере
    logging.info(f'{message.peer_id}: I get homework')
    try:
        # Получаем дз
        homework = db.get_homework(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            message.text
        )

        # Получаем дату обновления дз
        upd_date = db.get_upd_date(
            db.get_account_school(userInfo[0].id),
            db.get_account_class(userInfo[0].id),
            message.text
        )
    except TypeError:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Ты не зарегистрирован! \nНапиши "Начать"\n Или у тебя неверный логин/пароль')
        return

    await message.answer(f'Урок: {message.text} \nБыло обновлено: {upd_date} \nЗадание: {homework}')
    logging.info(f'{message.peer_id}: Send homework')



@bp.on.chat_message(payload={'cmd': 'homework'})
async def keyboard_schedule(message: Message):
    chat_id = message.chat_id
    logging.info(f'{message.peer_id}: I get homework')

    try:
        # Получаем дз
        homework = db.get_homework(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            message.text[30:]
        )

        # Получаем дату обновления дз
        upd_date = db.get_upd_date(
            db.get_chat_school(chat_id),
            db.get_chat_class(chat_id),
            message.text[30:]
        )
    except Exception as e:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer(f'Ошибка: {e} \nСообщи админу!')
        return

    await message.answer(f'Урок: {message.text[30:]} \nБыло обновлено: {upd_date} \nЗадание: {homework}')
    logging.info(f'{message.peer_id}: Send homework')