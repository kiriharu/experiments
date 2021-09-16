"""Простой скрипт для отправки нотификаций в сервисы (сейчас поддерживаются VK и Telegram)
Использование:
1) Импортируем в своем скрипте сервис и создаем его объект:
tg = Telegram("@somechannel", "bot_token")
2) Создаем объект нотификаций и пишем туда наши сервисы. Их может быть сколько угодно.
notify = Notify("bot1", [tg])
3) Отправляем сообщение!
notify.send("Error", "some exception occurred")
"""

__author__ = "https://github.com/kiriharu"
__copyright__ = "Copyright 2019, kiriharu"

import requests
from typing import List, Any
from random import randint


class IService:

    def __init__(self, target: Any, token: str, proxy: dict = None):
        """Конструктор класса сервисов для отправки

        :param target: кому отправляем
        :param token: Токен бота
        :param proxy: Прокси вида {"proto": "value"}
        """
        self.target = target
        self.token = token
        self.proxy = proxy

    def call(self, *args, **kwargs):
        """
        Метод вызова бота (например для отправки сообщения)
        """
        raise NotImplementedError

    def send(self, message: str):
        """Отправляем сообщение с сервиса

        :param message - сообщение
        """
        raise NotImplementedError


class Telegram(IService):

    def __init__(self, target, token: str, proxy: dict = None):
        super().__init__(target, token, proxy)

    def call(self, method: str, **kwargs):
        """Вызов методов сервиса

        :param method: метод для вызова
        :param kwargs: параметры для метода
        :return: ответ в формате json
        """
        return requests.get(f"https://api.telegram.org/bot{self.token}/{method}", params=kwargs, proxies=self.proxy).json()

    def send(self, message: str):
        """Отправка сообщения в Телеграм

        :param message: Сообщение для оправки
        :return: ответ сервера в json
        """
        params = {
            'chat_id': self.target,
            'text': message
        }
        return self.call('sendMessage', **params)


class VKontakte(IService):

    def __init__(self, target, token: str, proxy: dict = None):
        super().__init__(target, token, proxy)

    def call(self, method, args={}, **kwargs):
        """Вызов метода сервиса

        :param method: метод, который вызываем
        :param kwargs: аргументы для метода
        :param args: аргументы для метода
        :return: ответ в формате json
        """
        options = {
            "access_token": self.token,
            "v": "5.95"
        }
        options.update(args)
        options.update(kwargs)
        return requests.get('https://api.vk.com/method/' + method, params=options, proxies=self.proxy).json()

    def send(self, message: str):
        """Отправка сообщения в ВКонтакте

        :param message: сообщение.
        :return: ответ сервера
        """
        args = {
            "peer_id": self.target,
            "message": message,
            "random_id": randint(-0x7fffff, 0x7fffff)
        }
        return self.call('messages.send', args)


class Notify:

    def __init__(self, name: str, services: List):
        self.name = name
        self.services = services

    def send(self, notify_type, message):
        """
        Отправляет сообщения в сервисы вида [Name] [notify_type]: Message

        :param notify_type - тип сообщения (можно какой угодно, хоть notify, хоть exception)
        :param name - само сообщение
        """
        for service in self.services:
            service.send(f"[{self.name}] [{notify_type}]: {message}")
