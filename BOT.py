import requests
import vk_api
import random
#import enchant
#import difflib

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload 
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
#------------------------------------------------------------------------------------------------------------------------------
vk_session = vk_api.VkApi(token='2a5bf1964f96294db3b007d41e6cbd6d857eafdcea486c89f5689aac8024da071047163d85da6e920780f')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

upload = VkUpload(vk_session)
session = requests.Session()

random.seed(version=2) 
#------------------------------------------------------------------------------------------------------------------------------
def write_msg(event, message):
	if event.from_user:
		vk.messages.send( user_id=event.user_id, message=message, random_id=random.randint(1,999) )
	elif event.from_chat:
		vk.messages.send( chat_id=event.chat_id, message=message, random_id=random.randint(1,999) )

def att_msg(event, message, link):
	image = session.get(link, stream=True)
	photo = upload.photo_messages(photos=image.raw)[0]
	#attachments.append( 'photo{}_{}'.format(photo['owner_id'], photo['id']) )
	if event.from_user:
		vk.messages.send( user_id=event.user_id, attachment='photo{}_{}'.format(photo['owner_id'], photo['id']), message=message, random_id=random.randint(1,999) )
	elif event.from_chat:
		vk.messages.send( chat_id=event.chat_id, attachment='photo{}_{}'.format(photo['owner_id'], photo['id']), message=message, random_id=random.randint(1,999) )

def key_msg(event, message, keyboard):
	if event.from_user:
		vk.messages.send( user_id=event.user_id, message=message, keyboard=keyboard, random_id=random.randint(1,999) )
	elif event.from_chat:
		vk.messages.send( chat_id=event.chat_id, message=message, keyboard=keyboard, random_id=random.randint(1,999) )
#------------------------------------------------------------------------------------------------------------------------------
def create_keyboard():
	keyboard = vk_api.keyboard.VkKeyboard(inline=True)
	#False Если клавиатура должна оставаться откртой после нажатия на кнопку
	#True если она должна закрваться

	keyboard.add_button("Интернет", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	keyboard.add_button("ТВ", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button("Мобильная связь", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button("Домашний телефон", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	keyboard.add_line()
	keyboard.add_button("Видеонаблюдение", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)

	return keyboard.get_keyboard()

def create_empty_keyboard():
	keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
	return keyboard
#------------------------------------------------------------------------------------------------------------------------------

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:	
		text=event.text.lower()		
		if text == 'привет' or text == 'прив': #Если написали заданную фразу
			#print(event.user_id)
			user = vk.users.get(user_ids=event.user_id)
			name = user[0]['first_name']
			write_msg(event, "Привет, " + name)

		elif text == 'красава' or text == 'молодец': #Если написали заданную фразу
			#print(event.user_id)
			write_msg(event, "спс")

		elif text =='начать':
			key_msg(event, "Что Вас интересует?.", create_keyboard())

		elif 'интернет' in text:
			write_msg(event, "Запрос: интернет")
		elif 'тв' in text:
			write_msg(event, "Запрос: тв")		
		elif 'мобильная связь' in text:
			write_msg(event, "Запрос: связь")
		elif 'домашний телефон' in text:
			write_msg(event, "Запрос: телефон")
		elif 'видеонаблюдение' in text:
			write_msg(event, "Запрос: видеонаблюдение")

		else:
			write_msg(event, "Не понял...")
