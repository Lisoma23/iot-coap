"""Client d'observation CoAP (Module 2).

Le CLI `aiocoap-client --observe` (0.4.17) annule l'observation apres la
reponse initiale; ce script utilise l'API Python d'aiocoap, qui fonctionne.

Usage:
    python observe.py coap://localhost:5683/temp
    python observe.py -v coap://localhost:5683/temp   # affichage detaille des messages

Sortie normale:
    Valeur initiale: 22.5
    Notification: 23.1

Sortie detaillee (-v): en plus de la valeur, les messages CoAP echanges
(initiation de l'observation puis notifications) sont affiches, comme avec
l'option -v de coap-client dans le sujet.
"""
import argparse
import asyncio
import logging
import sys

import aiocoap
from aiocoap import error

logging.basicConfig(format="%(message)s", stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("coap.observe")


def message_to_text(m, direction):
    """Texte court decrivant un message CoAP, sur le modele du sujet."""
    lines = []
    if getattr(m, "code", None) is not None:
        lines.append("v:1 t:%s c:%s %s" % (m.mtype.name, m.code, direction))
    for opt in m.opt.option_list():
        if hasattr(opt.number, "name"):
            lines.append("  [%s]" % opt.number.name_printable)
    if m.payload:
        text = m.payload.decode(errors="replace")
        lines.append("  payload: %r" % text)
    return "\n".join(lines)


async def main():
    parser = argparse.ArgumentParser(description="Client d'observation CoAP")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="affiche les messages CoAP échangés")
    parser.add_argument("uri", nargs="?", default="coap://localhost:5683/temp")
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.CRITICAL + 1)

    ctx = await aiocoap.Context.create_client_context()
    request = ctx.request(aiocoap.Message(code=aiocoap.GET, uri=args.uri, observe=0))

    initial = await request.response
    if args.verbose and initial is not None:
        log.info(message_to_text(initial, "ACK (initiation de l'observation)"))
    print("Valeur initiale: %s" % initial.payload.decode(), flush=True)

    try:
        async for notification in request.observation:
            if args.verbose and notification is not None:
                log.info(message_to_text(notification, "CON (notification)"))
            print("Notification: %s" % notification.payload.decode(), flush=True)
    except (error.NotObservable, error.ObservationCancelled):
        print("Observation terminée par le serveur.", file=sys.stderr)
    finally:
        await ctx.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
