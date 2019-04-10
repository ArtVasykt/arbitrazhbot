import betgrab
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, ReplyKeyboardMarkup
from random import choice
from time import sleep
import json

TOKEN = '844914308:AAGaJiIHBTV8d-84DgZbRsDU7qQO_8WFSvE'
PROXY = 'https://185.80.130.17:80'
GROUP = '-1001494021764'
OFFER = 'http://tr.delaidelami.ru/click?pid=1379&offer_id=132'

authorized_admins = []
admin_statuses = {}

with open('messages.json', 'r', encoding='utf-8-sig') as f:
	MESSAGES = json.load(f)

def updatemessages(typo, text):
	with open('messages.json', 'w', encoding='utf-8-sig') as f:
		if typo == 1:
			MESSAGES['betinfo'].append(text)
		elif typo == 2:
			MESSAGES['morning'].append(text)
		elif typo == 3:
			MESSAGES['evening'].append(text)
		f.write(json.dumps(MESSAGES, ensure_ascii=False, sort_keys=True, indent=4))

def viewmessage(chat_id, view):
	bot.sendMessage(chat_id, 'Вот такие вот пироги🥞')
	for index, v in enumerate(MESSAGES[view]):
		bot.sendMessage(chat_id, v, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[dict(text='Удалить♻️', callback_data='delete_{0}_{1}'.format(view, index))]]))

def on_callback(msg):
	query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
	if 'delete' in data:
		data = data.split('_')
		with open('messages.json', 'w', encoding='utf-8-sig') as f:
			MESSAGES[data[1]].pop(int(data[2]))
			f.write(json.dumps(MESSAGES, ensure_ascii=False, sort_keys=True, indent=4))
		bot.sendMessage(from_id, 'Успешно удалено!')

def chat(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	if msg['text'] == "БЕТБОТ123":
		authorized_admins.append(chat_id)
		admin_statuses[chat_id] = 'idle'
		bot.sendMessage(chat_id, "Режим админа активирован!🛐", reply_markup=ReplyKeyboardMarkup(keyboard=[["Сообщения📲"],['Расписание⏰']]))
	else:
		if chat_id in authorized_admins:
			if msg['text'] == "Сообщения📲":
				bot.sendMessage(chat_id,
				 "В данное время есть:\n\nИнформация ставки💴 - {0}\nПриветствия днем🌄 - {1}\nПриветствия вечером🌇 - {2}".format(
				 	len(MESSAGES['betinfo']), len(MESSAGES['morning']), len(MESSAGES['evening'])), reply_markup=ReplyKeyboardMarkup(keyboard=[
				 	['Создать новую✅', 'Просмотреть👁‍🗨']]))

			elif msg['text'] == 'Просмотреть👁‍🗨':
				bot.sendMessage(chat_id, "Что вы хотите посмотреть, милорд?🖕🏾", reply_markup=ReplyKeyboardMarkup(keyboard=[
					['Информация ставки💴'],['Приветствие днем🌄'],['Приветствие вечером🌇']]))
				admin_statuses[chat_id] = 'view'

			elif msg['text'] == 'Информация ставки💴' and admin_statuses[chat_id] == 'view':
				viewmessage(chat_id, 'betinfo')

			elif msg['text'] == 'Приветствие днем🌄' and admin_statuses[chat_id] == 'view':
				viewmessage(chat_id, 'morning')

			elif msg['text'] == 'Приветствие вечером🌇' and admin_statuses[chat_id] == 'view':
				viewmessage(chat_id, 'evening')



			elif msg['text'] == "Создать новую✅":
				admin_statuses[chat_id] = 'messages'
				bot.sendMessage(chat_id, "Что вы хотите создать, милорд?🖕🏾", reply_markup=ReplyKeyboardMarkup(keyboard=[
					['Информация ставки💴'],['Приветствие днем🌄'],['Приветствие вечером🌇']]))

			elif msg['text'] == 'Информация ставки💴' and admin_statuses[chat_id] == 'messages':
				bot.sendMessage(chat_id, "Пишите.\nНо обратите внимание.\n\n{0} - дата\n{1} - тэги\n{2} - первая команда\n{3} - вторая команда\n{4} - прогноз")
				admin_statuses[chat_id] = 'typo1'

			elif msg['text'] == 'Приветствие днем🌄' and admin_statuses[chat_id] == 'messages':
				bot.sendMessage(chat_id, "Пишите.")
				admin_statuses[chat_id] = 'typo2'

			elif msg['text'] == 'Приветствие вечером🌇' and admin_statuses[chat_id] == 'messages':
				bot.sendMessage(chat_id, "Пишите.")
				admin_statuses[chat_id] = 'typo3'



			elif msg['text'] == 'Расписание⏰':
				pass


			else:
				if admin_statuses[chat_id] == 'typo1':
					updatemessages(1, msg['text'])
				if admin_statuses[chat_id] == 'typo2':
					updatemessages(2, msg['text'])
				if admin_statuses[chat_id] == 'typo3':
					updatemessages(3, msg['text'])
				admin_statuses[chat_id] = 'idle'
				bot.sendMessage(chat_id, "Режим админа!🛐", reply_markup=ReplyKeyboardMarkup(keyboard=[["Сообщения📲"],['Расписание⏰']]))

def sendbets():
	bets = betgrab.grab()
	for bet in bets:
		markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='Поставить💸', url=OFFER)]])
		bot.sendPhoto(GROUP, photo=bet['pfc'])
		bot.sendPhoto(GROUP, photo=bet['psc'])
		bot.sendMessage(GROUP, choice(MESSAGES['betinfo']).format(bet['date'], bet['tags'], bet['first_command'], bet['second_command'], bet['prediction']),reply_markup=markup)
		# {0} - дата {1} - тэги {2} - первая команда {3} - вторая команда {4} - прогноз

#telepot.api.set_proxy(PROXY)
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'callback_query': on_callback, 'chat': chat}).run_as_thread()
while True:
	sendbets()
	print('Засыпаем на 1.5 минуты')
	sleep(100000)