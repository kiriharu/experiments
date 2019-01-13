"""Данная утилита предназначена для скачивания файлов с имиджборды 2ch.hk."""

import requests
import traceback

def content_from_thread():
    try:
        threadlink = input('Enter link to thread like https://2ch.hk/board/res/threadid.json: ')
        getpost = requests.get(threadlink).json()
    except:
        print('Exception occurred: ', traceback.format_exc())
    for threads in getpost['threads']:
        for posts in threads['posts']:
            for files in posts['files']:
                try:
                    with open(files['fullname'], "wb") as file:
                        getfile = requests.get('https://2ch.hk/' + files['path'])
                        file.write(getfile.content)
                        file.close()
                        print('Saved file: ', files['fullname'])
                except IOError:
                    print('Path not found or permission denied')
    exit('All downloaded!')

def all_content_from_board():
    bname =  input('Enter board name: ')
    print('All files will saved to the folder, where script is saved ')
    for i in range(1, 10):
        if i == 1:
            i = 'index'
        try:
            getthreads = requests.get('https://2ch.hk/%s/%s.json' % (bname, i)).json()
            print('Getting https://2ch.hk/%s/%s.json' % (bname, i))
            for thread in getthreads['threads']:
                thread_num = thread['thread_num']
                getposts = requests.get('https://2ch.hk/%s/res/%s.json' % (bname, thread_num)).json()
                for threads in getposts['threads']:
                    for posts in threads['posts']:
                        for files in posts['files']:
                            try:
                                with open(files['fullname'], "wb") as file:
                                    getfile = requests.get('https://2ch.hk/' + files['path'])
                                    file.write(getfile.content)
                                    file.close()
                                    print('Saved file: ', files['fullname'])
                            except IOError:
                                print('Path not found or permission denied')
        except:
            print(traceback.format_exc())
    exit('All downloaded!')

def main():
    reply = input('Welcome to 2ch content downloader! Enter the option that you need\n'
          '1) Download content from board\n'
          '2) Download content from thread\n')
    if reply == '1':
        all_content_from_board()
    if reply == '2':
        content_from_thread()
    else:
        print('Please type 1 or 2.')
        main()

if __name__ == '__main__':
    main()

