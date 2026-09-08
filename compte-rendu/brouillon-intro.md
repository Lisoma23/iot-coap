# Compte rendu - CoAP pour l'IoT (brouillon)

> Sections proposées. À valider puis intégrer dans le compte rendu final.
> L'utilisation de « nous » (pluriel de rédaction) est à confirmer selon les conventions attendues par le professeur.

---

## 1. Environnement de travail

### 1.1 Contexte du TP

Le sujet initial prévoyait l'utilisation de l'image Docker `coapcloud/coap` pour le serveur et le client CoAP. Cette image ayant été retirée de Docker Hub, nous avons mis en place un environnement alternatif sur la base de la librairie Python `aiocoap`, conforme au conseil du professeur.

### 1.2 Architecture mise en place

L'environnement se compose de deux éléments :

- un **serveur CoAP** Python (`aiocoap`) exécuté dans un conteneur Docker, qui simule un objet connecté (capteur de température, LED, journaux) et expose les ressources du TP : `/time`, `/temp`, `/led`, `/logs`, `/biglog`, ainsi que l'annuaire `/.well-known/core` ;
- un **client CoAP** en ligne de commande, `aiocoap-client`, installé sur la machine locale grâce à la librairie `aiocoap`.

Le serveur se lance avec Docker Compose :

```sh
docker compose up -d --build
```

Il écoute sur le port standard CoAP 5683 (UDP), exposé sur la machine hôte via le mapping `5683:5683/udp`. La communication client-serveur se fait donc sur `coap://localhost:5683`.

Le client s'installe sur la machine avec :

```sh
pip install aiocoap
```

puis s'utilise de la forme :

```sh
aiocoap-client [options] coap://localhost:5683/<ressource>
```

_Suite du compte rendu : modules 1, 2, 3 et conclusion._
