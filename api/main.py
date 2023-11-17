from fastapi import FastAPI, HTTPException, Path
import mysql.connector
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="pokemondb"
)

def insert_pokemons():
    cursor = db.cursor()

    with open('./data/pokemon.json', 'r') as file:
        pokemons_data = json.load(file)

    for pokemon_info in pokemons_data['pokemon']:
        pokemon_id = pokemon_info['id']
        numero_pokedex = pokemon_info['numero_pokedex']
        nom = pokemon_info['nom']
        taille = pokemon_info['taille']
        poids = pokemon_info['poids']
        statistiques_base = pokemon_info['statistiques_base']
        image = pokemon_info['image']

        query = "SELECT * FROM Pokemon WHERE id = %s"
        cursor.execute(query, (pokemon_id,))

        if not cursor.fetchone():
            insert_query = """
                INSERT INTO Pokemon (id, numero_pokedex, nom, taille, poids, statistiques_base, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (pokemon_id, numero_pokedex, nom, taille, poids, statistiques_base, image))

            for type_id in pokemon_info['types']:
                insert_type_query = "INSERT INTO Pokemon_Type (pokemon_id, type_id) VALUES (%s, %s)"
                cursor.execute(insert_type_query, (pokemon_id, type_id))

            for competence_id in pokemon_info['competences']:
                insert_competence_query = "INSERT INTO Pokemon_Competence (pokemon_id, competence_id) VALUES (%s, %s)"
                cursor.execute(insert_competence_query, (pokemon_id, competence_id))

    db.commit()

def insert_competences():
    cursor = db.cursor()

    with open('./data/competences.json', 'r') as file:
        competences_data = json.load(file)

    for competence_info in competences_data['competences']:
        competence_id = competence_info['id']
        competence_nom = competence_info['nom']
        competence_description = competence_info['description']
        competence_puissance = competence_info['puissance']
        competence_precision = competence_info['precision']
        competence_pp_max = competence_info['pp_max']
        type_id = competence_info['type_id']

        query = "SELECT * FROM Competence WHERE id = %s"
        cursor.execute(query, (competence_id,))

        if not cursor.fetchone():
            insert_query = """
                INSERT INTO Competence (id, nom, description, puissance, precision_value, pp_max, type_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (competence_id, competence_nom, competence_description, competence_puissance, competence_precision, competence_pp_max, type_id))

    db.commit()

def insert_type():
    cursor = db.cursor()
    
    with open('./data/types.json', 'r') as file:
        types_data = json.load(file)
        
    for type_info in types_data['types']:
        type_id = type_info['id']
        type_name = type_info['nom']

        # Vérifier si le type existe déjà
        query = "SELECT * FROM Type WHERE id = %s"
        cursor.execute(query, (type_id,))

        if not cursor.fetchone():
            # Le type n'existe pas, l'insérer
            insert_query = "INSERT INTO Type (id, nom) VALUES (%s, %s)"
            cursor.execute(insert_query, (type_id, type_name))
    db.commit()

@app.on_event("startup")
def import_data_on_startup():
    insert_type()
    insert_competences()
    insert_pokemons()

class Pokemon:
    def __init__(self, id, numero_pokedex, nom, taille, poids, statistiques_base, image, types, competences):
        self.id = id
        self.numero_pokedex = numero_pokedex
        self.nom = nom
        self.taille = taille
        self.poids = poids
        self.statistiques_base = statistiques_base
        self.image = image
        self.types = types
        self.competences = competences
        
class NewPokemon(BaseModel):
    id: int
    numero_pokedex: int
    nom: str
    taille: float
    poids: float
    statistiques_base: str
    image: str
    types: List[str]
    competences: List[str]

class NewType(BaseModel):
    nom: str
        
class UpdatePokemon(BaseModel):
    nom: str
    taille: float
    poids: float
    statistiques_base: str
    image: str
    types: List[int]
    competences: List[int]

class UpdateAbility(BaseModel):
    nom: str
    description: str
    puissance: int
    precision: int
    pp_max: int
    type_id: int
        
class UpdateType(BaseModel):
    nom: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/pokemons")
def get_all_pokemons():
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT p.id, p.numero_pokedex, p.nom, p.taille, p.poids, p.statistiques_base, p.image,
                   GROUP_CONCAT(DISTINCT t.nom) AS types,
                   GROUP_CONCAT(DISTINCT c.nom) AS competences
            FROM Pokemon p
            LEFT JOIN Pokemon_Type pt ON p.id = pt.pokemon_id
            LEFT JOIN Type t ON pt.type_id = t.id
            LEFT JOIN Pokemon_Competence pc ON p.id = pc.pokemon_id
            LEFT JOIN Competence c ON pc.competence_id = c.id
            GROUP BY p.id
        """

        cursor.execute(query)
        pokemons_data = cursor.fetchall()

        pokemons = []
        for pokemon_data in pokemons_data:
            pokemon = Pokemon(
                id=pokemon_data["id"],
                numero_pokedex=pokemon_data["numero_pokedex"],
                nom=pokemon_data["nom"],
                taille=pokemon_data["taille"],
                poids=pokemon_data["poids"],
                statistiques_base=pokemon_data["statistiques_base"],
                image=pokemon_data["image"],
                types=pokemon_data["types"].split(",") if pokemon_data["types"] else [],
                competences=pokemon_data["competences"].split(",") if pokemon_data["competences"] else [],
            )
            pokemons.append(pokemon)


        return pokemons

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/pokemons/{pokemon_id}")
def get_pokemon_details(pokemon_id: int = Path(..., title="ID du Pokémon à récupérer")):
    try:
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT p.id, p.numero_pokedex, p.nom, p.taille, p.poids, p.statistiques_base, p.image,
                   GROUP_CONCAT(DISTINCT t.nom) AS types,
                   GROUP_CONCAT(DISTINCT c.nom) AS competences
            FROM Pokemon p
            LEFT JOIN Pokemon_Type pt ON p.id = pt.pokemon_id
            LEFT JOIN Type t ON pt.type_id = t.id
            LEFT JOIN Pokemon_Competence pc ON p.id = pc.pokemon_id
            LEFT JOIN Competence c ON pc.competence_id = c.id
            WHERE p.id = %s
            GROUP BY p.id
        """

        cursor.execute(query, (pokemon_id,))
        pokemon_data = cursor.fetchone()

        if not pokemon_data:
            raise HTTPException(status_code=404, detail="Pokémon non trouvé")

        pokemon = Pokemon(
            id=pokemon_data["id"],
            numero_pokedex=pokemon_data["numero_pokedex"],
            nom=pokemon_data["nom"],
            taille=pokemon_data["taille"],
            poids=pokemon_data["poids"],
            statistiques_base=pokemon_data["statistiques_base"],
            image=pokemon_data["image"],
            types=pokemon_data["types"].split(",") if pokemon_data["types"] else [],
            competences=pokemon_data["competences"].split(",") if pokemon_data["competences"] else [],
        )

        return pokemon

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/types/{type_id}")
def get_type_details(type_id: int = Path(..., title="ID du Type à récupérer")):
    try:
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM Type WHERE id = %s"
        cursor.execute(query, (type_id,))
        type_data = cursor.fetchone()

        if not type_data:
            raise HTTPException(status_code=404, detail="Type non trouvé")


        return type_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/abilities")
def get_all_abilities():
    try:
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM Competence"
        cursor.execute(query)
        abilities = cursor.fetchall()

        return abilities

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pokemons")
def add_pokemon(new_pokemon: NewPokemon):
    try:
        cursor = db.cursor()

        insert_pokemon_query = """
            INSERT INTO Pokemon (numero_pokedex, nom, taille, poids, statistiques_base, image)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_pokemon_query, (
            new_pokemon.numero_pokedex, new_pokemon.nom, new_pokemon.taille,
            new_pokemon.poids, new_pokemon.statistiques_base, new_pokemon.image
        ))

        new_pokemon_id = cursor.lastrowid

        for type_id in new_pokemon.types:
            insert_type_query = "INSERT INTO Pokemon_Type (pokemon_id, type_id) VALUES (%s, %s)"
            cursor.execute(insert_type_query, (new_pokemon_id, type_id))

        for competence_id in new_pokemon.competences:
            insert_competence_query = "INSERT INTO Pokemon_Competence (pokemon_id, competence_id) VALUES (%s, %s)"
            cursor.execute(insert_competence_query, (new_pokemon_id, competence_id))

        db.commit()

        return {"message": "Pokémon ajouté avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/types")
def add_type(new_type: NewType):
    try:
        cursor = db.cursor()

        insert_type_query = "INSERT INTO Type (nom) VALUES (%s)"
        cursor.execute(insert_type_query, (new_type.nom,))

        db.commit()

        return {"message": "Type ajouté avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/api/pokemons/{pokemon_id}")
def update_pokemon(pokemon_id: int = Path(..., title="ID du Pokémon à modifier"), update_data: UpdatePokemon = None):
    try:
        cursor = db.cursor()

        update_pokemon_query = """
            UPDATE Pokemon
            SET nom = %s, taille = %s, poids = %s, statistiques_base = %s, image = %s
            WHERE id = %s
        """
        cursor.execute(update_pokemon_query, (
            update_data.nom, update_data.taille, update_data.poids,
            update_data.statistiques_base, update_data.image, pokemon_id
        ))

        delete_types_query = "DELETE FROM Pokemon_Type WHERE pokemon_id = %s"
        cursor.execute(delete_types_query, (pokemon_id,))

        for type_id in update_data.types:
            insert_type_query = "INSERT INTO Pokemon_Type (pokemon_id, type_id) VALUES (%s, %s)"
            cursor.execute(insert_type_query, (pokemon_id, type_id))

        delete_competences_query = "DELETE FROM Pokemon_Competence WHERE pokemon_id = %s"
        cursor.execute(delete_competences_query, (pokemon_id,))

        for competence_id in update_data.competences:
            insert_competence_query = "INSERT INTO Pokemon_Competence (pokemon_id, competence_id) VALUES (%s, %s)"
            cursor.execute(insert_competence_query, (pokemon_id, competence_id))

        db.commit()


        return {"message": "Pokémon modifié avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/api/abilities/{ability_id}")
def update_ability(ability_id: int = Path(..., title="ID de la compétence à modifier"), update_data: UpdateAbility = None):
    try:
        cursor = db.cursor()

        update_ability_query = """
            UPDATE Competence
            SET nom = %s, description = %s, puissance = %s, precision = %s, pp_max = %s, type_id = %s
            WHERE id = %s
        """
        cursor.execute(update_ability_query, (
            update_data.nom, update_data.description, update_data.puissance,
            update_data.precision, update_data.pp_max, update_data.type_id, ability_id
        ))

        db.commit()

        return {"message": "Compétence modifiée avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/types/{type_id}")
def update_type(type_id: int = Path(..., title="ID du type à modifier"), update_data: UpdateType = None):
    try:
        cursor = db.cursor()

        update_type_query = "UPDATE Type SET nom = %s WHERE id = %s"
        cursor.execute(update_type_query, (update_data.nom, type_id))

        db.commit()

        return {"message": "Type modifié avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.delete("/api/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int = Path(..., title="ID du Pokémon à supprimer")):
    try:
        cursor = db.cursor()

        check_pokemon_query = "SELECT * FROM Pokemon WHERE id = %s"
        cursor.execute(check_pokemon_query, (pokemon_id,))
        existing_pokemon = cursor.fetchone()

        if not existing_pokemon:
            raise HTTPException(status_code=404, detail="Pokémon non trouvé")

        delete_pokemon_query = "DELETE FROM Pokemon WHERE id = %s"
        cursor.execute(delete_pokemon_query, (pokemon_id,))

        db.commit()

        return {"message": "Pokémon supprimé avec succès"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))