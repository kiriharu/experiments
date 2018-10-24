#!/usr/bin/env python3
#Требуется вот эта библиотека https://github.com/satoshi03/pings
#Сам скрипт очень простой - просто пингует айпишники раз в 60 секунд. True - ответ есть, False - нет.
import pings
import datetime
import time

nodes = {
	'192.168.1.1' : 'Server - 1',
	'8.8.8.8' : 'google.com'
}
p = pings.Ping()
print('Last check: {}'.format(datetime.datetime.now()))
while True:
	for node, info in nodes.items():
		response = p.ping(node)
		print('Node {node} ({info}) -> {status}'.format(node = node, info = info, status = response.is_reached()))
	print('Done! Waiting next check...')
	time.sleep(60)