## This script simply send message to Telegram chats.
## Works with nim 0.20
## Compile: nim c -d:ssl -d:release


import httpclient, json, parseopt, strutils

const API_URL = "https://api.telegram.org/"


type
    TelegramBot = ref object of RootObj
        token: string

proc TelegramAPIRequest(this: TelegramBot, apimethod: string, data: MultipartData): JsonNode =
    let client = newHttpClient(maxRedirects=0)
    let request = API_URL & this.token & '/' & apimethod
    return parseJson(client.postContent(request, multipart=data))

proc sendMessage(this: TelegramBot, chat_id: string, text: string): bool =
    var data = newMultipartData()
    data.add("text", text)
    data.add("chat_id", chat_id)
    when defined(parse_mode):
        data.add("parse_mode", parse_mode)
    var request = TelegramAPIRequest(this, "sendMessage", data)
    if request["ok"].getBool():
        return true
    else:
        return false

proc getHelp() =
    echo """
    
    tgsender by kiriharu (nim version, tested on 0.20.0v)
    -t | --token     : bot token. Example: bot1235123132:AaAXFASafsksalfsafisaoS
    -c | --chats     : chats to post message. Example: 1592102138213,29213831201
    -m | --message   : message to send
    -h | --help      : show this message

    USAGE: tgsender --token=bot1235123132:AaAXFASafsksalfsafisaoS --chats=-1592102138213,29213831201 --message="Hello from tgsender!"
    
    """
 
proc main() =

    var 
        token: string = ""
        Bot = TelegramBot(token: token)
        chats = newSeq[string]()
        message = ""


    for kind, key, val in getopt():
        case kind
        of cmdLongOption, cmdShortOption:
            case key
            of "help", "h":
                getHelp()
            of "token", "t":
                token = val
                Bot = TelegramBot(token: token)
            of "chats", "c":
                for chat in val.split(','):
                    echo chat
                    chats.add(chat)
            of "message", "m":
                message = val
            else:
                getHelp()
        else:
            getHelp()
    for chat in chats:
        echo sendMessage(Bot, chat, message)

when isMainModule:
    main()