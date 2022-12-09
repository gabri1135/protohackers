import asyncio
import logging


class ChatGroup:
    def __init__(self) -> None:
        self.data = dict()

    def insert(self, name: str, w: asyncio.StreamWriter) -> bool:
        if name in self.data.keys():
            return False
        self.data[name] = w
        self.send(name, f"* {name} has entered the room\n")
        #logging.debug(f"--* {name} join the group")
        return True

    def remove(self, name: str) -> None:
        t = self.data.pop(name, -1)
        if t != -1:
            self.send(name, f"* {name} has left the room\n")
        #logging.debug(f"--* {name} left the group")

    def getUsers(self, name: str) -> str:
        return ", ".join(u for u in self.data.keys() if u != name)

    def send(self, fromUser: str, d: str | bytes):
        if isinstance(d, str):
            d = d.encode("utf8")
        for user, w in self.data.items():
            if user != fromUser:
                w.write(d)
        logging.debug(d)

    def sendMessage(self, fromUser: str, text: str) -> None:
        self.send(fromUser, f"[{fromUser}] {text}\n")


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    name = None
    try:
        w.write(b"Welcome to budgetchat! What shall I call you?\n")
        name = (await r.readuntil(b'\n')).decode("utf8").strip()
        if not name.isalnum() or not name:
            raise ValueError()
        if not chat.insert(name, w):
            raise KeyError()

        w.write(f"* The room contains: {chat.getUsers(name)}\n".encode("utf8"))
        logging.debug(
            f"* The room contains: {chat.getUsers(name)}\n".encode("utf8"))

        while not r.at_eof():
            message = (await r.readuntil(b'\n')).decode("utf8").strip()
            chat.sendMessage(name, message)
    except asyncio.IncompleteReadError:
        if name:
            chat.remove(name)
    except ValueError:
        logging.debug(f"Invalid username: {name}")
    except KeyError:
        logging.debug("Username already exists")
    else:
        chat.remove(name)
    await w.drain()
    w.close()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5001)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()

chat = ChatGroup()

if __name__ == '__main__':
    asyncio.run(main())
