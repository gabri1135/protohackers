from asyncio import open_connection, run


async def main():
    r, w = await open_connection("vcs.protohackers.com", 30307)
    # r,w=await open_connection('0.0.0.0',5000)
    w.write(b"put /g 5\n")
    w.write(b"\x86cia\n")
    await r.readuntil(b"ERR")
    print(await r.readuntil(b"\n"))
    print(await r.readuntil(b"\n"))
    w.write(b"put /g 5\n")
    w.write(b"ciao\n")
    print(await r.readuntil(b"\n"))
    print(await r.readuntil(b"\n"))


if __name__ == "__main__":
    run(main())
