#!/usr/bin/env python3
#Небольшая утилита для отправки сообщений/файлов через бота telegram. Используется из шела.
import sys
import telebot
#telebot используется этот https://github.com/eternnoir/pyTelegramBotAPI/
from telebot import util
from telebot import apihelper
import argparse
#apihelper.proxy = Прокси, если надо.
token = 'Сюда токен от бота'
chat_id = 'Сюда id чата, в который будем всё отсылать. Chat ID также можно задавать при помощи --chat_id'
bot = telebot.TeleBot(token)
parser = argparse.ArgumentParser(
    prog='tgsender',
    description='Send messages and files via telegram bot')
parser.add_argument('--text',
    help='Text to send')
parser.add_argument('--parse_mode',
    help='Message parsing mode',
    default='markdown')
parser.add_argument('--chat_id',
    help='Chat ID',
    default=chat_id)
parser.add_argument('--file',
	help='path to file',
	default=None)

args = parser.parse_args()

#Если количество аргументов равно 1 (просто pinger.py) - показываем help и выходим.
if len(sys.argv) == 1:
	parser.print_help()
	exit()

#Если в аргуметах есть --file открываем и отсылаем его как документ.
if args.file:
	data = open(args.file, 'rb')
	bot.send_document(chat_id, data)

#Если в аргументах есть --text...
if args.text:
	try:
		#Пытаемся его отправить обычным методом.
		bot.send_message(args.chat_id,
	    args.text,
	    parse_mode=args.parse_mode)
	except:
		#Если сообщение слишком длинное
		splitted_text = util.split_string(args.text, 3000)
		for text in splitted_text:
			#Не используем markdown, ибо это может вызвать ошибки :shrug
			bot.send_message(chat_id, text)
