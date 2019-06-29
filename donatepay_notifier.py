import requests
from time import sleep
import os
from random import randint

# Donatepay Notifier
# Получает последний донат и постит информацию о нём.


class IBot:
    """Интерфейс (можно смеяться) для ботов."""

    def __init__(self, token, target):
        """

        :param token: Токен бота
        :param target: Куда постим
        """
        self.token = token
        self.target = target

    def post(self, message):
        """
        Постинг сообщения ботом.

        :param message: сообщение.
        """
        raise NotImplementedError


class Telegram(IBot):

    def __init__(self, token: str, target: str, proxy: dict=None):
        """

        :param token: токен вида 123456789:AAAAAAA_Xxxxxxxxxxxxxxxxxxxxxx
        :param target: chat_id, место постинга
        :param proxy: прокси сервера в dict вида {"proto": "value"}
        Для прокси нужен pySocks
        """
        super().__init__(token=token, target=target)
        self.proxy = proxy

    def call(self, method: str, **kwargs):
        """
        Вызов метода бота

        :param method: метод, который вызываем
        :param kwargs: аргументы для метода
        :return: ответ в формате json
        """
        return requests.get(f"https://api.telegram.org/bot{self.token}/{method}", params=kwargs, proxies=self.proxy).json()

    def post(self, message):
        """
        Постинг сообщения ботом.

        :param message: сообщение.
        :return: ответ сервера
        """
        params = {
            'chat_id': self.target,
            'text': message
        }
        return self.call('sendMessage', **params)


class VK(IBot):

    def __init__(self, token, target):
        super().__init__(token=token, target=target)

    def call(self, method, args={}, **kwargs):
        """
        Вызов метода бота

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
        return requests.get('https://api.vk.com/method/' + method, params=options).json()

    def post(self, message):
        """
        Постинг сообщения ботом.

        :param message: сообщение.
        :return: ответ сервера
        """
        args = {
            "peer_id": self.target,
            "message": message,
            "random_id": randint(-0x7fffff, 0x7fffff)
        }
        return self.call('messages.send', args)


class DonatePay:

    def __init__(self, token, bots: list=None, timer=90):
        self.token = token
        self.timer = timer
        self.bots = bots

    def request(self, limit=None, before=None, after=None, skip=None, order=None, type="donation", status="success"):
        """

        :param limit: Лимит записей (По умолчанию: 25. Максимальное значение: 100)
        :param before: Вывод будет осуществляться до указанного ID транзакции
        :param after: Вывод будет осуществляться после указанного ID транзакции
        :param skip: Сколько транзакций пропустить
        :param order: Сортировка транзакций (ASC - По возрастанию; DESC - по убыванию) [По умолчанию: DESC]
        :param type: Тип транзакции ("donation" - Пожертвование, "cashout" - Вывод средств)
        :param status: Статус транзакции ("success" - Успешно, "cancel" - Ошибка, "wait" - Ожидание, "user" -
        Пользовательская [Тестовые пожертвования])
        :return: ответ в формате json
        """
        url = "https://donatepay.ru/api/v1/transactions"
        params = {
            "access_token": self.token,
            "limit": limit,
            "before": before,
            "after": after,
            "skip": skip,
            "order": order,
            "type": type,
            "status": status
        }
        req = requests.get(url, params=params)
        return req.json()

    @property
    def last_id_and_data(self):
        """
        :return: Возвращает последний id и данные ответа
        """
        data = self.request()
        last = [item['id'] for item in data['data']][0]
        return last, data

    def loop(self):
        """
        Основной луп скрипта
        :return: None
        """

        last = 0

        # Проверяем, есть ли lastid
        if os.path.exists("lastid"):
             with open("lastid", "r") as f:
                last = f.read()
        # Если нет - записываем lastid в свежий файл
        else:
            with open("lastid", "w") as f:
                last = self.last_id_and_data[0]
                f.write(str(last))
        while True:
            print(f"Последний id {last}")
            try:
                sleep(self.timer)
                # Получаем свежие данные
                getlast, data = self.last_id_and_data
                if isinstance(last, str):
                    last = int(last)
                if getlast > last:
                    pay = data['data'][0]
                    message = f"Спасибо огромное {pay['what']} за {pay['sum']}!\nКомментарий: {pay['comment']}"
                    # Отправляем все через ботов
                    for bot in self.bots:
                        bot.post(message)
                    print(message)
                    # Присваиваем текущий id последнему
                    last = getlast
                    # Сохраняем его в файл
                    with open("lastid", "w") as f:
                        if isinstance(last, int):
                            last = str(last)
                        f.write(last)
            except Exception as e:
                print(f"Exception occurred: {e}")


if __name__ == "__main__":
    # Загружаем проксички, например {'https': socks5:testpass@127.0.0.1:228'}
    proxy = {}
    # Инициализируем бота для Telegram
    tg = Telegram("токен сюда", "сюда чат или канал", proxy)
    # Инициализируем бота для ВКонтакте
    vk = VK('токен сюда', "сюда чат, id пользователя и т.д.")
    # В bots укажите только те объекты ботов, которые настроены и вам нужны. По умолчанию включены оба.
    # Если вы хотите оставить (например) только Телеграм-бота, напишите bots=[tg]
    d = DonatePay("токен donatepay", bots=[tg, vk])
    # Запускаем бесконечный луп
    d.loop()
