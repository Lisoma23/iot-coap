# Iot - CoAP

Projet EFREI - M2 DEV1 - Culture des concepts informatiques

## Sujet

CoAP pour l'IoT : comprendre le protocole Constrained Application Protocol, et mettre en place un environnement de test avec Docker Compose (client/serveur CoAP).

## Contenu

- `server.py` : serveur CoAP Python (librairie [`aiocoap`](https://github.com/chrysn/aiocoap))
- `Dockerfile` : image du serveur
- `docker-compose.yml` : lancement du serveur CoAP
- `compte-rendu/` : compte rendu à rédiger

Le sujet est disponible via l'issue de suivi du projet et les échanges sur les issues.

## Modules

1. **Module 1** : Premiers pas avec CoAP (GET, POST, PUT, DELETE)
2. **Module 2** : L'observation (OBSERVE) - la grande force de CoAP
3. **Module 3** : Découverte des ressources et Blockwise

## Installation / mise en route

> Note : l'image Docker `coapcloud/coap` a été retirée de Docker Hub. On utilise un serveur CoAP Python (`aiocoap`).

Lancer le serveur (port UDP 5683) :

```
docker compose up -d --build
```

Le client en ligne de commande (`aiocoap-client`) est fourni avec la librairie :

```
pip install aiocoap
aiocoap-client coap://localhost:5683/time
```

> Sous Docker Desktop (macOS), un message « Response arrived from different address » peut s'afficher en plus de la réponse : il est dû au NAT Docker et sans impact.

Les commandes détaillées par module sont dans les issues de suivi (issues #1, #2, #3).

## Équipe

Travail en équipe via GitHub Issues. Chaque module et le compte rendu ont leur propre issue de suivi.
