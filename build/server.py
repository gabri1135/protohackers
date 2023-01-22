import asyncio
import logging

from voracious_code_storage.dirFile import Directory
from voracious_code_storage.parseRequests import *


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    async def read():
        return (await r.readline()).strip().decode('utf-8')

    async def readExactly(length):
        return (await r.readexactly(length)).decode('utf-8')

    async def write(data, end=True):
        data = data if isinstance(data, bytes)else data.encode('utf-8')
        w.write(data)
        if end:
            w.write(b'\n')
        await w.drain()

    while not r.at_eof():
        try:
            await write('READY')
            data = await read()
            method, *_ = data.split(' ')
            logging.debug(f'\n--> {data}')

            if method.upper() == 'PUT':
                path, length = parsePut(data)
                text = await readExactly(length)
                version = dir.put(path, text)
                await write(f'OK {version}')
                logging.debug(f'<--OK {version}')

            elif method.upper() == 'GET':
                path, version = parseGet(data)
                text, length = dir.get(path, version)
                await write(f'OK {length}')
                await write(text, end=False)
                logging.debug(f'<--OK {length}')

            elif method.upper() == 'LIST':
                path = parseList(data)
                lista = dir.lista(path)
                lista.sort()
                print(lista)
                await write(f'OK {len(lista)}')
                await write('\n'.join(lista))
                logging.debug(f'<--OK {len(lista)}')

            elif method.upper() == 'HELP':
                await write('OK usage: HELP|GET|PUT|LIST')
            else:
                if method:
                    raise BadRequest(f'illegal method: {method}', True)

        except BadRequest as e:
            logging.warning(e.message)
            await write(f'ERR {e.message}')
            if e.eof:
                r.feed_eof()
        except UnicodeDecodeError:
            logging.warning('text files only')
            await write(f'ERR text files only')
        except asyncio.IncompleteReadError:
            pass
        except ConnectionResetError:
            break

    w.close()

dir = Directory()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()
