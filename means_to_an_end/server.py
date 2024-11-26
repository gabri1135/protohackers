import asyncio
import logging
import struct


class HistoricalPrice:
    def __init__(self) -> None:
        self.data = dict()

    def insert(self, time: int, price: int) -> None:
        self.data[time] = price

    def avg(self, minTime: int, maxTime: int) -> int:
        tot = 0
        rec = 0
        for x in self.data.keys():
            if minTime <= x <= maxTime:
                tot += self.data[x]
                rec += 1
        return tot // rec if rec != 0 else 0


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    def write(d: int):
        w.write(struct.pack("!i", d))
        logging.debug(f"--> {d}")

    historicalPrice = HistoricalPrice()

    while not r.at_eof():
        try:
            method, a, b = struct.unpack("!cii", await r.readexactly(9))
            logging.debug(f"<-- {method} {a} {b}")

            if method == b"I":
                historicalPrice.insert(a, b)
            elif method == b"Q":
                write(historicalPrice.avg(a, b))
            else:
                raise ValueError()

        except (asyncio.IncompleteReadError, ValueError):
            write(-1)
            break
    await w.drain()
    w.close()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5001)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
