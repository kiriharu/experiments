#!/usr/bin/env python3
"""
Данная утилита предназначена для скачивания файлов с имиджборды 2ch.hk.

Created by https://github.com/kiriharu
Re-writed by https://github.com/undefinedvalue0103
"""
import requests
import traceback
import re

def download_file(fileobject: dict):
    """
    Download file. Parameters given in file object
    @param fileobject: dict{path,fullname,md5}
    """
    url = "https://2ch.hk" + fileobject["path"]
    fallback = fileobject["name"]
    name = fileobject["md5"] + " " + fileobject.get("fullname", fallback)
    try:
        with open(name, "wb") as fd:
            with requests.get(url, stream=True) as rq:
                expected_size = int(rq.headers.get("Content-Length", 1))
                downloaded = 0
                for chunk in rq.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                    progress = downloaded / expected_size
                    width = int(progress * 10)
                    line = "[I] %35s: [%s%s] %7.3f%%" % (fileobject["path"],
                                                     "=" * width,
                                                     " " * (10 - width),
                                                     progress * 100)
    
                    print(line, end="\r", flush=1)
                    fd.write(chunk)
                    fd.flush()
    except IOError as e:
        print("[E] Filed to open file %r: %r" % (name, e))
    except Exception as e:
        print("[E] Exception occurred: %r" % e)
    else:
        print("")

def iter_files(board: str, thread: int=None, status:str=None):
    """
    Yields files from thread
    @param board: str, board letters (example, 'b')
    @param thread: int/None, thread ID. If ommited, all threads given.
    @param status: str/None, status string. used for progress

    @returns generator(fileobject:dict)
    """
    if thread is not None:
        thread_url = f"https://2ch.hk/{board}/res/{thread}.json"
        print("[I] Getting", thread_url, status or "")
        data = requests.get(thread_url).json()
        for thread in data["threads"]:
            for post in thread["posts"]:
                for fileobj in post["files"]:
                    if fileobj["type"] != 100:
                        yield fileobj
    else:
        for index in range(1, 10):
            index = "index" if index == 1 else index
            page_url = f"https://2ch.hk/{board}/{index}.json"
            print("[I] Getting", page_url)
            data = requests.get(page_url).json()
            threads = len(data["threads"])
            for i, thread in enumerate(data["threads"], 1):
                thread_num = thread["thread_num"]
                for fileobj in iter_files(board, thread_num, "%3d/%3d"%(i, threads)):
                    yield fileobj

def main():
    print("Welcome to 2chdownloader!")
    print("Type board name as 'name' for downloading entire board")
    print("Type thread as 'board/thread' for downloading one thread")
    print("Type 'exit' for exit")
    while True:
        line = input("> ")
        if line == "exit":
            return
        elif re.match(r"^(\w+)$", line):
            for fileobj in iter_files(line):
                download_file(fileobj)
            print("[I] Done")
        elif re.match(r"^(\w+)\/(\d+)$", line):
            board, thread = line.split("/")
            for fileobj in iter_files(board, int(thread)):
                download_file(fileobj)
            print("[I] Done")
        else:
            print("Something went wrong")
        

if __name__ == '__main__':
    main()

