"""Client d'observation CoAP (Module 2).

Le CLI `aiocoap-client --observe` (0.4.17) annule l'observation apres la
reponse initiale; ce script utilise l'API Python d'aiocoap, qui fonctionne.

Usage:
    python observe.py coap://localhost:5683/temp
"""
import asyncio
import sys

import aiocoap


async def main():
    uri = sys.argv[1] if len(sys.argv) > 1 else "coap://localhost:5683/temp"
    ctx = await aiocoap.Context.create_client_context()
    request = ctx.request(aiocoap.Message(code=aiocoap.GET, uri=uri, observe=0))

    initial = await request.response
    print("Valeur initiale:", initial.payload.decode(), flush=True)

    try:
        async for notification in request.observation:
            print("Notification:", notification.payload.decode(), flush=True)
    finally:
        await ctx.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
