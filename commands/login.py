from vkbottle.bot import Message
from vkbottle.bot import Blueprint
from PostgreSQLighter import db
import ns
import logging



bp = Blueprint('login')# Объявляем команду
bp.on.vbml_ignore_case = True # Игнорируем регистр




#Если написали "Вход" или нажали на соответствующую кнопку
@bp.on.private_message(text=["Вход <userLogin> <userPassword>", "Вход", 'Войти', 'Войти <userLogin> <userPassword>'])
@bp.on.private_message(payload={'cmd': 'login'})
async def private_login(message: Message, userLogin=None, userPassword=None):
    logging.info(f'{message.peer_id}: I get login')
    userInfo = await bp.api.users.get(message.from_id) # Информация о юзере

    # Если человека нет в бд
    if db.get_account_isFirstLogin(userInfo[0].id) is None:
        logging.info(f'{message.peer_id}: User not in database')
        await message.answer("Так... Смотрю тебя теще нет в моей бд. Но ничего страшного сейчас все будет!")
        await message.answer('Напиши "Начать')
        return

    #Если пароль и логин введены
    if userLogin != None and userPassword != None:
        #Записать их в бд
        db.edit_account_login(userInfo[0].id, userLogin)
        db.commit()
        db.edit_account_password(userInfo[0].id, userPassword)
        db.commit()
        db.edit_account_studentId(userInfo[0].id, 
            await ns.getCurrentStudentId(
                userLogin,
                userPassword, 
                db.get_account_school(userInfo[0].id),
                db.get_account_link(userInfo[0].id)))
        db.commit()
        db.edit_account_correctData(userInfo[0].id, 0)
        db.commit()
        logging.info(f'{message.peer_id}: Write new data to database')

    
    #Записываем логин из бд в переменную
    userLogin = db.get_account_login(userInfo[0].id)
    userPassword = db.get_account_password(userInfo[0].id)
    userSchool = db.get_account_school(userInfo[0].id)
    userLink = db.get_account_link(userInfo[0].id)
    studentId = db.get_account_studentId(userInfo[0].id)

    try:
        #Авторезируемся в Сетевом Городе
        await ns.login(
            userLogin,
            userPassword,
            userSchool,
            userLink,
            studentId
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!')
        return

    db.edit_account_correctData(userInfo[0].id, 1) #Подтверждаем правильность логина и пароя в бд
    db.commit()
    logging.info(f'{message.peer_id}: Write correctData to database')

    await message.answer(f'{userInfo[0].first_name}, ты успешно зашел в систему под логином: {userLogin}')
    logging.info(f'{message.peer_id}: login COMPLETED')
    #Выходим из СГ
    #await ns.logout(userLink)

    #Спустя 10 минут удаляем из памяти дневник ученика
    #await asyncio.sleep(600)
    #diarys.pop(userInfo[0].id)
    #await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')




@bp.on.chat_message(text=["Вход <userLogin> <userPassword>", "Вход"])
@bp.on.chat_message(payload={'cmd': 'login'})
async def chat_login(message: Message, userLogin=None, userPassword=None):
    logging.info(f'{message.peer_id}: I get login')
    chat_id = message.chat_id # Чат айди

    try:

        #Если пароль и логин введены
        if userLogin != None and userPassword != None:
            #Записать их в бд
            db.edit_chat_login(chat_id, userLogin)
            db.commit()
            db.edit_chat_password(chat_id, userPassword)
            db.commit()
            db.edit_chat_studentId(chat_id, 
            await ns.getCurrentStudentId(
                userLogin,userPassword, 
                db.get_chat_school(chat_id),
                db.get_chat_link(chat_id)))
            logging.info(f'{message.peer_id}: Write new data to database')

        
        #Записываем логин из бд в переменную
        chatLogin = db.get_chat_login(chat_id)
        #Записываем пароль из бд в переменную
        chatPassword = db.get_chat_password(chat_id)
        #Записываем школу из бд в переменную
        chatSchool = db.get_chat_school(chat_id)
        #Записываем ссылку из бд в переменную
        chatLink = db.get_chat_link(chat_id)
        #Записываем id ученика из бд в переменную
        studentId = db.get_chat_studentId(chat_id)

        #Авторезируемся в Сетевом Городе
        await ns.login(
            chatLogin,
            chatPassword,
            chatSchool,
            chatLink,
            studentId
        )
        logging.info(f'{message.peer_id}: Login in NetSchool')
            
    except TypeError:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Нужно зарегистрировать беседу. \nНапиши "Начать"')
        return

    except:
        logging.exception(f'{message.peer_id}: Exception occurred')
        await message.answer('Неправильный логин или пароль!')
        return

    await message.answer(f'Эта беседа успешно зашла в систему под логином: {chatLogin}')
    logging.info(f'{message.peer_id}: login COMPLETED')
    #Выходим из СГ
    #await ns.logout()

    #Спустя 10 минут удаляем из памяти дневник ученика
    #await asyncio.sleep(600)
    #diarys.pop(userInfo[0].id)
    #await message.answer('Ты был отключен от системы, из-за длительного пребывания в ней')
