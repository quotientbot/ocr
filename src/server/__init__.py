from __future__ import annotations

from .app import init_application
from aiohttp import web


class StartServer:
    app: web.Application
    app_started: bool = False
    webserver: web.TCPSite

    async def start_application(self):
        self.app, self.webserver = await init_application()
        self.app_started = True

    async def close_application(self):
        if self.app_started:
            await self.webserver.stop()
            await self.app.shutdown()
            await self.app.cleanup()
            self.task.cancel()


async def main(server: StartServer, **kwargs):
    await server.start_application()
