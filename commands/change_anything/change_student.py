from vkbottle.bot import Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import logging
import ns
from VKRules import PayloadStarts


bp = Blueprint('change_student')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр
bp.labeler.custom_rules["PayloadStarts"] = PayloadStarts





@bp.on.private_message(payload={'cmd': 'change_student'})
async def private_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    students = await ns.getStudents(
        db.get_account_login(user_id),
        db.get_account_password(user_id),
        db.get_account_school(user_id),
        db.get_account_link(user_id),
        db.get_account_studentId(user_id)
    )
    currentStudentId = db.get_account_studentId(user_id)
    
    keyboard = Keyboard()
    for i in students:
        if i['studentId'] == currentStudentId:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        else:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
            keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери ребенка', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent change_student')

@bp.on.chat_message(payload={'cmd': 'change_student'})
async def chat_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student')
    # Айди чата:
    chat_id = message.chat_id

    students = await ns.getStudents(
        db.get_chat_login(chat_id),
        db.get_chat_password(chat_id),
        db.get_chat_school(chat_id),
        db.get_chat_link(chat_id),
        db.get_chat_studentId(chat_id)
    )
    currentStudentId = db.get_chat_studentId(chat_id)
    
    keyboard = Keyboard()
    for i in students:
        if i['studentId'] == currentStudentId:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
        else:
            keyboard.add(Text(i['nickName'], {'cmd': f'change_student_{i["studentId"]}'}), color=KeyboardButtonColor.SECONDARY)
            keyboard.row()
    keyboard.add(Text("Назад", {'cmd': 'change_anything_kb'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Выбери ребенка', keyboard=keyboard)
    logging.info(f'{message.peer_id}: I sent change_student')


@bp.on.private_message(PayloadStarts='{"cmd":"change_student_')
async def private_exactly_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    # Информация о юзере
    userInfo = await bp.api.users.get(message.from_id) 
    user_id = userInfo[0].id

    studentId = message.payload[23:-2]

    db.edit_account_studentId(user_id, studentId)

    await message.answer('Я успешно сменил выбранного ребенка')
    logging.info(f'{message.peer_id}: I sent change_student with studentId')
    await private_change_student(message)

@bp.on.chat_message(PayloadStarts='{"cmd":"change_student_')
async def chat_exactly_change_student(message: Message):
    logging.info(f'{message.peer_id}: I get change_student with studentId')
    # Айди чата:
    chat_id = message.chat_id

    studentId = message.payload[23:-2]

    db.edit_chat_studentId(chat_id, studentId)

    await message.answer('Я успешно сменил выбранного ребенка')
    logging.info(f'{message.peer_id}: I sent change_student with studentId')
    await chat_change_student(message)