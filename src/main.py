from server import StartServer, main
import asyncio

if __name__ == "__main__":
    server = StartServer()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(server))
    loop.run_forever()
