import asyncio
import json
import logging
import math


def isPrime(n: int | float) -> bool:
    if n < 2 or type(n) == float:
        return False

    i = 2
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i += 1 + i % 2
    return True


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    def write_json(d):
        w.write(json.dumps(d).encode())
        w.write(b"\n")
        logging.debug(f"--> {d}")

    while not r.at_eof():
        try:
            data = json.loads((await r.readuntil(b"\n")).decode())
            logging.debug(f"<-- {data}")
            method = data["method"]
            number = data["number"]

            if method != "isPrime" or not type(number) in (int, float):
                write_json({"error": "invalid_json"})
                break

            write_json({"method": "isPrime", "prime": isPrime(number)})
        except asyncio.IncompleteReadError:
            write_json({"error": "invalid_terminator"})
            break
        except (KeyError, json.decoder.JSONDecodeError):
            write_json({"error": "invalid_json"})
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
