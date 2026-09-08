"""Serveur CoAP minimal pour le TP - utilise la librairie aiocoap.

Fonctionne seul avec la commande:
    python server.py
et répond sur le port standard CoAP 5683/UDP.
"""
import asyncio
import time

import aiocoap
from aiocoap.resource import Resource, ObservableResource, Site, WKCResource
from aiocoap import Message


class TimeResource(Resource):
    async def render_get(self, request):
        return Message(payload=time.strftime("%Y-%m-%dT%H:%M:%SZ").encode())


class TempResource(ObservableResource):
    def __init__(self):
        super().__init__()
        self.value = "22.5"
        self.deleted = False

    def set(self, value):
        self.value = value
        self.updated_state()

    async def render_get(self, request):
        if self.deleted:
            raise aiocoap.error.NotFound()
        return Message(payload=self.value.encode())

    async def render_put(self, request):
        if self.deleted:
            raise aiocoap.error.NotFound()
        self.set(request.payload.decode())
        return Message(code=aiocoap.CHANGED)

    async def render_delete(self, request):
        self.deleted = True
        return Message(code=aiocoap.DELETED)


class LedResource(Resource):
    def __init__(self):
        super().__init__()
        self.state = "off"

    async def render_get(self, request):
        return Message(payload=self.state.encode())

    async def render_put(self, request):
        self.state = request.payload.decode()
        return Message(code=aiocoap.CHANGED)

    async def render_delete(self, request):
        self.state = "off"
        return Message(code=aiocoap.DELETED)


class LogsResource(Resource):
    def __init__(self):
        super().__init__()
        self.logs = []

    async def render_get(self, request):
        return Message(payload="\n".join(self.logs).encode())

    async def render_post(self, request):
        entry = "{} - {}".format(
            time.strftime("%Y-%m-%dT%H:%M:%SZ"), request.payload.decode()
        )
        self.logs.append(entry)
        return Message(code=aiocoap.CREATED)


class BigLogResource(Resource):
    def __init__(self):
        super().__init__()
        self.data = b""

    async def render_put(self, request):
        self.data = request.payload
        return Message(code=aiocoap.CHANGED)

    async def render_get(self, request):
        return Message(payload=self.data)


def main():
    root = Site()
    root.add_resource(["time"], TimeResource())
    root.add_resource(["temp"], TempResource())
    root.add_resource(["led"], LedResource())
    root.add_resource(["logs"], LogsResource())
    root.add_resource(["biglog"], BigLogResource())
    root.add_resource([".well-known", "core"], WKCResource(root.get_resources_as_linkheader))

    asyncio.run(serve(root))


async def serve(root):
    await aiocoap.Context.create_server_context(root, ("0.0.0.0", 5683))
    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    main()
