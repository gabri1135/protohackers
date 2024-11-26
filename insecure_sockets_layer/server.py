import asyncio
import logging

from cipher import *


async def buildSpec(r: asyncio.StreamReader) -> list[Cipher]:
    ciph = []
    while True:
        s = (await r.readexactly(1))[0]
        if s == 0:
            break
        elif s == 1:
            ciph.append(ReverseBits())
        elif s == 2:
            ciph.append(Xor((await r.readexactly(1))[0]))
        elif s == 3:
            ciph.append(XorPos())
        elif s == 4:
            ciph.append(Add((await r.readexactly(1))[0]))
        elif s == 5:
            ciph.append(AddPos())
        else:
            raise ValueError()
    return ciph


async def handle(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    def enc(data: bytes) -> bytes:
        for a in ciph:
            data = a.encode(data)
        return data

    def dec(data: bytes | int) -> bytes:
        if isinstance(data, int):
            data = data.to_bytes(1, "big")
        for a in ciph[::-1]:
            data = a.decode(data)
        return data

    try:
        ciph = await buildSpec(r)
        logging.debug("Spec loaded")

        while not r.at_eof():
            encData = b""
            bDecData = b""
            while True:
                encData += await r.readexactly(1)
                bDecData += dec(encData[-1])
                if bDecData.endswith(b"\n"):
                    break
            assert bDecData != encData
            decData = bDecData.decode("ascii")
            # logging.debug(f'<-- {decData}')

            # toys = re.findall(r'(\d*)x ([\w\- ]*)', decData)
            toys = decData.strip().split(",")
            toy = max(toys, key=lambda x: int(x.split("x")[0]))
            decData = f"{toy}\n".encode("ascii")

            assert decData != (encData := enc(decData))
            w.write(encData)
            await w.drain()
            logging.debug(f"--> {decData}")

    except asyncio.IncompleteReadError:
        pass
    except AssertionError:
        logging.debug(f"plain equal to cipher")
    w.close()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    server = await asyncio.start_server(handle, "0.0.0.0", 5000)
    logging.debug("Server ready")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
