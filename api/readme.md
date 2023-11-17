---
runme:
  id: 01HFFCCRRRYDME4MHH683BPWC9
  version: v2.0
---

# Projet Pokémon API

Ce projet consiste en une API FastAPI pour gérer des informations sur les Pokémon, telles que les détails des Pokémon, les types et les compétences.

## Configuration de l'environnement

1. Assurez-vous d'avoir Python installé. Si ce n'est pas le cas, téléchargez-le depuis [python.org](https://www.python.org/).

2. Installez les dépendances à l'aide de la commande suivante :
   ```bash
   pip install -r requirements.txt

## Configuration de la base de données
1. Assurez-vous que votre serveur MySQL est en cours d'exécution.

2. Créez une base de données nommée pokemondb.

3. Exécutez les scripts SQL fournis dans le dossier sql/ pour créer les tables nécessaires.

## Lancement de l'application
```bash
    uvicorn main:app --reload
```
L'API sera accessible à l'adresse http://127.0.0.1:8000.

## Endpoints API
### Ajout d'un Pokémon
- **Méthode HTTP** : POST

- **URL** : /api/pokemons

- **Données attendues** : Les détails du nouveau Pokémon au format JSON.


### Suppression d'un Pokémon
- **Méthode HTTP** : DELETE

- **URL** : /api/pokemons/{id}

- **Paramètre** : id représente l'ID du Pokémon à supprimer..


### Modification d'un Pokémon
- **Méthode HTTP** : PUT

- **URL** : /api/pokemons/{id}

- **Paramètre** : id représente l'ID du Pokémon à modifier.

- **Données attendues** : Les détails mis à jour du Pokémon au format JSON.


### Liste de tous les Pokémon
- **Méthode HTTP** : GET

- **URL** : /api/pokemons


### Liste de tous les types
- **Méthode HTTP** : GET

- **URL** : /api/types


### Liste de toutes les compétences
- **Méthode HTTP** : GET

- **URL** : /api/abilities