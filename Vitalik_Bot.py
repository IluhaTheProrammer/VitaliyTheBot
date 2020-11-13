import requests
import vk_api
import random
import wikipedia #Модуль Википедии

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload 
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
#------------------------------------------------------------------------------------------------------------------------------
vk_session = vk_api.VkApi(token='2a5bf1964f96294db3b007d41e6cbd6d857eafdcea486c89f5689aac8024da071047163d85da6e920780f')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

#attachments = []
cats=["https://im0-tub-ru.yandex.net/i?id=2a5389e33580f37889eed9d122d7872e&n=13", 
      "https://w-dog.ru/wallpapers/5/18/289291145046987/evropejskaya-koshka-dikij-kot-morda-vzglyad.jpg",
      "https://im0-tub-ru.yandex.net/i?id=ce0895303f9763615dfb10ad03f5c207&n=13",
      "https://im0-tub-ru.yandex.net/i?id=2f76b890c67b578f1faa2796fd7c4f16&n=13",
      "https://im0-tub-ru.yandex.net/i?id=05b966298cf6e5444dbdf0ca43cdac63&n=13",
      "https://im0-tub-ru.yandex.net/i?id=0e7e67cfa5f4a9f2f618ef05273cd112&n=13"]
dogs=["https://animalsik.com/wp-content/uploads/2016/05/velsh-korgi-5-e1462947298660.jpg",
      "https://ural-meridian.ru/wp-content/uploads/2018/04/Sobaka.jpg",
      "https://im0-tub-ru.yandex.net/i?id=f219a104ffb7321fd1b3727ebd77876f&n=13",
      "https://w-dog.ru/wallpapers/16/15/334049107693169/alyaskinskij-malamut-sobaka-lajka.jpg",
      "https://avatars.mds.yandex.net/get-zen_doc/225409/pub_5ccec106e520c700b3216c29_5ccec4f54c5e42046d153c81/scale_1200",
      "https://im0-tub-ru.yandex.net/i?id=f88506c2c3e7b7690885ca8c248e65f4&n=13"]

upload = VkUpload(vk_session)
session = requests.Session()

random.seed(version=2) 
wikipedia.set_lang("RU")
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
	keyboard = vk_api.keyboard.VkKeyboard(one_time=False, inline=True)
	#False Если клавиатура должна оставаться откртой после нажатия на кнопку
	#True если она должна закрваться

	keyboard.add_button("Закрыть", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
	keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)

	keyboard.add_line()#Обозначает добавление новой строки
	keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)

	keyboard.add_line()
	keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
	keyboard.add_button("Кнопка", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)

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

		elif text == 'кот': 
			#print(event.user_id)
			att_msg(event, "Мяу!", random.choice(cats))

		elif text == 'пёс' or text == 'пес': 
			#print(event.user_id)
			att_msg(event, "Гав!", random.choice(dogs))

		elif text == 'красава' or text == 'молодец': #Если написали заданную фразу
			#print(event.user_id)
			write_msg(event, "спс")

		elif text =='клава':
			key_msg(event, "Открываю.", keyboard_1.get_keyboard())
		elif text =='закрыть':
			key_msg(event, "Закрываю.", create_empty_keyboard())				

		else:
			write_msg(event, "Не понял...")
