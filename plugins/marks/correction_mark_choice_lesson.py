from typing import Text
from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from sqlighter import SQLighter
from vkbottle import Keyboard, KeyboardButtonColor, Text


bp = Blueprint('correction_mark_choice_lesson') # Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр сообщений

db = SQLighter('database.db')# Подключаемся к базеданных


@bp.on.message(payload={'cmd': 'correction_mark_choice_lesson'})
async def correction_mark_choice_lesson(message: Message):
    #Создаем клавиатуру
    keyboard = (
        Keyboard()
        #Добавить кнопку
        .add(Text('Алгебра', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Инф.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Геом.', {"cmd": "correction_mark_choice_mark"}))
        #Начать с новой строки
        .row()
        .add(Text('Рус. яз.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Англ. яз.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Литература', {"cmd": "correction_mark_choice_mark"}))
        .row()
        .add(Text('Родн.Рус. яз.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Родн. лит-ра', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('ОБЖ', {"cmd": "correction_mark_choice_mark"}))
        .row()
        .add(Text('Общество.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('История', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Геогр.', {"cmd": "correction_mark_choice_mark"}))
        .row()
        .add(Text('Биол.', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Физика', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Химия', {"cmd": "correction_mark_choice_mark"}))
        .row()
        .add(Text('Музыка', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Физ-ра', {"cmd": "correction_mark_choice_mark"}))
        .add(Text('Техн.', {"cmd": "correction_mark_choice_mark"}))
        .row()
        .add(Text("Назад", {'cmd': 'marks'}), color=KeyboardButtonColor.NEGATIVE)
    )

    await message.answer('Какой предмет хочешь исправить?', keyboard=keyboard)