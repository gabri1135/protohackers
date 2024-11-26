import asyncio
import logging


async def serve(rx: asyncio.StreamReader, tx: asyncio.StreamWriter):
    tx.write(await rx.read())
    await tx.drain()
    tx.close()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(serve, "0.0.0.0", 5001)

    logging.debug("starting server")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
