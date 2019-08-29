#Simple site checker.

import httpclient, os, strformat, terminal, net, locks, sequtils

proc CheckLink(link: string, c: HttpClient): tuple[valid: bool, code: int] =
    try:
        var status = c.request(link).code
        case status
            of HttpCode(200): return (true, 200)
            of HttpCode(500): return(false, 500)
            of HttpCode(403): return(false, 403)
            of HttpCode(301): return(true, 301)
            of HttpCode(302): return(true, 302)
            of HttpCode(400): return(false, 400)
            of HttpCode(410): return(false, 410)
            else: return (false, 999)
    except OSError:
        return (false, 404)
    except TimeoutError:
        return (false, 404)
    except ValueError:
        return CheckLink("http://" & link, c)
    except ProtocolError:
        return (false, 404)

proc openfile(filename: string): File =
    if not existsFile(filename):
        open(filename, fmWrite).close()
    return open(filename, fmWrite)

proc LinksLoader(filename: string): seq[string] =
    var iter = 0
    var links = newSeq[string]()
    for link in lines filename:
        iter += 1
        links.add(link)
    echo fmt"Loaded {iter} links!"
    return links

proc Checker(links: seq[string], c: HttpClient): void {.thread.} =
    var resp: (bool, int)
    var good = openfile("good.txt")
    var bad = openfile("bad.txt")
    for line in links:
        resp = CheckLink(line, c)
        if resp[0] == true:
            setForegroundColor(fgGreen)
            echo fmt"[Success] [{resp[1]}] {line} "
            good.writeLine(line)
        else:
            setForegroundColor(fgRed)
            echo fmt"[  Fail ] [{resp[1]}] {line} "
            bad.writeLine(line)
    good.close()
    bad.close()
    echo "Checked!"

when isMainModule:

    var loadedfile = LinksLoader("links.txt")
    var client = newHttpClient(maxRedirects = 3, timeout = 500)

    Checker(loadedfile, client)