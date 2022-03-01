from server import StartServer, main
import asyncio

if __name__ == "__main__":
    server = StartServer()
    asyncio.run(main(server,))