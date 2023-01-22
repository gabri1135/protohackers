from badRequest import BadRequest
from re import fullmatch


def parsePut(data: str) -> tuple[list[str], int]:
    if not fullmatch(r'PUT .+ .+', data.upper()):
        raise BadRequest('usage: PUT file length newline data')
    _, name, *lengths = data.split(' ', 2)
    checkFile(name)
    length=checkLength(lengths)
    path = name.split('/')
    return path, length


def parseGet(data: str) -> tuple[list[str], int]:
    if not fullmatch(r'GET .+[ .+]?', data.upper()):
        raise BadRequest('usage: GET file [revision]')
    _, name, *ver = data.split(' ',2)
    checkFile(name)
    version=checkVersion(ver)
    return name.split('/'), version


def parseList(data: str) -> list[str]:
    if not fullmatch(r'LIST .+', data.upper()):
        raise BadRequest('usage: LIST dir')
    _, *name = data.split(' ',1)
    checkDir(name[0])
    return name[0].split('/')


def checkFile(name: str) -> None:
    if not name.startswith('/'):
        raise BadRequest('illegal file name')
    if name.endswith('/'):
        raise BadRequest('illegal file name')
    if not fullmatch(r'(\/[a-zA-Z0-9._\-]+)+', name):
        raise BadRequest('illegal file name')


def checkDir(name: str) -> None:
    if not name.startswith('/'):
        raise BadRequest('illegal dir name')


def checkLength(ver: list[str]) -> int:
    if len(ver) == 0:
        raise BadRequest('usage: PUT file length newline data')
    elif fullmatch(r'[0-9]+', ver[0]):
        return int(ver[0])
    else:
        raise BadRequest('usage: GET file [revision]')

def checkVersion(ver:list[str])->int:
    if len(ver) == 0:
        return -1
    elif fullmatch(r'r[0-9]+', ver[0]):
        return int(ver[0].removeprefix('r'))
    else:
        raise BadRequest('usage: GET file [revision]')
