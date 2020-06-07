# Обычная небольшая постилка для 2ch.hk
# Необходим requests чтобы слать данные в эти ваши интернеты. Ставится через pip install requests
# Без поддержки капчи. Возможно, запилю потом.
# Пример использования описан ниже

import requests


class Post:
    POSTING_URL = "https://2ch.hk/makaba/posting.fcgi?json=1"

    def __init__(self, board: str, thread: int):
        self.params = []
        self._headers = {}
        self.board = board
        self.thread = thread
        self.init_default_params()

    def __call__(self):
        return requests.post(
            self.POSTING_URL, files=self.params, headers=self._headers
        ).json()

    def init_default_params(self):
        params = dict(
            task=(None, "post"),
            board=(None, self.board),
            thread=(None, self.thread),
            usercode=(None, ""),
            code=(None, "")
        )
        for key, val in params.items():
            self.params.append((key, val))

    def headers(self, headers: dict):
        self._headers = headers
        return self

    def text(self, comment: str):
        self.params.append(
            ("comment", (None, comment))
        )
        return self

    def subject(self, subject: str):
        self.params.append(
            ("comment", (None, subject))
        )
        return self


if __name__ == "__main__":
    # simple usage
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--board", help="Board to post")
    parser.add_argument("-n", "--numthread", type=int, help="Thread to post")
    parser.add_argument("-t", "--text", help="Text to post")
    args = parser.parse_args()

    board = args.board
    thread = args.numthread
    text = args.text

    if not args.board or not args.numthread or not args.text:
        print("Usage: python3 simple_2ch_poster.py -b b -n 1 -t=Bump!")
        exit(-1)

    headers = {
        "Host": "2ch.hk",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Accept": "application/json, text/javasctipt, */*; q=0.01",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://2ch.hk/{board}/res/{thread}.html",
        "X-Requested-With": "XMLHttpRequest", "Cookie": "", "Connection": "close", "UPGRADE-INSECURE-REQUESTS": "1",
        "DNT": "1"
    }

    print(Post(board, thread).text(text).headers(headers)())
