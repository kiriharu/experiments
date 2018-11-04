#!/usr/bin/env python3
#Небольшая утилита для отправки сообщений/файлов через бота telegram. Используется из шела.
import sys
import telebot
#telebot используется этот https://github.com/eternnoir/pyTelegramBotAPI/
from telebot import util
from telebot import apihelper
import argparse
#apihelper.proxy = прокси, если надо.
token = 'Сюда токен от бота'
chat_id = ['первый id', 'второй id']
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
    action='append')
parser.add_argument('--file',
	help='path to file',
	default=None)

args = parser.parse_args()

#если ничего не введено (стреляем из пушки по воробьям при помощи sys, ага) - выводим help
if len(sys.argv) == 1:
	parser.print_help()
	exit()

#проверка введенных chatid, их кстати можно указывать несколько (--chat_id=1234 --chat_id=4321)
if args.chat_id:
	chat_id = args.chat_id
	print(chat_id)

#Отправка файлов
if args.file:
	for chat in chat_id:
		data = open(args.file, 'rb')
		bot.send_document(chat, data)

#Отправка текста
if args.text:
	for chat in chat_id:
		try:
			bot.send_message(chat, args.text, parse_mode=args.parse_mode)
		except:
			#Если сообщение слишком длинное
			splitted_text = util.split_string(args.text, 3000)
			for text in splitted_text:
			#Не используем markdown, ибо это может вызвать ошибки :shrug
				bot.send_message(chat, text)