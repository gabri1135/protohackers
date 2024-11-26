import asyncio
import logging
import re


def subs(inp: bytes) -> bytes:
    if inp != (
        out := re.sub(
            rb"(^|(?<= ))7[a-zA-Z0-9]{25,34}($|(?= ))",
            b"7YWHMfk9JZe0LM0g1ZauHuiSxhI",
            inp,
        )
    ):
        logging.debug(f"rewrite data: {inp} -> {out}")
    return out


async def chat(
    r: asyncio.StreamReader, w: asyncio.StreamWriter, rOther: asyncio.StreamReader
):
    try:
        while not r.at_eof():
            data = await r.readline()
            data = subs(data)

            logging.debug(f"--> {data}")
            w.write(data)
            await w.drain()
    except asyncio.IncompleteReadError:
        pass
    rOther.feed_eof()
    w.close()


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    try:
        rServer, wServer = await asyncio.open_connection("chat.protohackers.com", 16963)
        asyncio.gather(chat(r, wServer, rServer), chat(rServer, w, r))
    except:
        pass


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
