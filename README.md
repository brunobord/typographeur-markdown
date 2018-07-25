# Typographeur / Markdown

> Faire respecter les règles typographiques françaises en Markdown.

Ce paquetage offre la possibilité d'appliquer un certain nombre de règles de typographie française sur des documents écrits en Markdown (ou plus précisément le Markdown de Github, celui qui inclut les tableaux et les blocs de code bornés par des contre-quotes).

Il utilise les règles implémentées dans le paquet [`typographeur`](https://github.com/brunobord/typographeur).

**Prenez garde !** Certains types de balisages complexes en Markdown, notamment les tableaux, nécessitent que le fichier fourni en entrée soit réécrit avant d'être renvoyé dans la sortie standard. Il se peut que le programme en ligne de commande "saccage" quelque peu votre document source, aussi nous recommendons de prendre garde à ne pas écraser votre travail d'origine.

Compatibilité : Python 3.6 et 3.7.

Dépendances :

* `mistune`: parser Markdown,
* `typographeur`: la bibliothèque en charge de faire respecter les règles de typographie.

## Installation

Comme d'autres paquets Python, Typographeur / Markdown s'installe à l'aide de ``pip``, de préférence dans un ``virtualenv``.

[Clonez ce dépôt Github](https://github.com/brunobord/typographeur-markdown) et installez-le en mode "dev" dans l'environnement courant :

```sh
git clone git@github.com:brunobord/typographeur-markdown.git
cd typographeur-markdown
pip install -e ./
```

## Utilisation

La bibliothèque n'en est qu'à un stade primitif, elle est loin d'être fonctionnelle et se contente pour le moment de renvoyer le contenu en Markdown remanié par le parser `mistune` intégré. Il va falloir être patient !
