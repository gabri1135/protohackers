import asyncio
import logging

async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    try:
        None
    except asyncio.IncompleteReadError:
        pass
    await w.drain()
    w.close()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
