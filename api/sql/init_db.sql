CREATE TABLE Pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_pokedex INT,
    nom VARCHAR(255),
    taille FLOAT,
    poids FLOAT,
    statistiques_base VARCHAR(255),
    image VARCHAR(255)
);

CREATE TABLE Type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255)
);

CREATE TABLE Competence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    `description` VARCHAR(255),
    puissance INT,
    precision_value INT,
    pp_max INT
);

CREATE TABLE Pokemon_Type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pokemon_id INT,
    type_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (type_id) REFERENCES Type(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Pokemon_Competence (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pokemon_id INT,
    competence_id INT,
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (competence_id) REFERENCES Competence(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Competence_Type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    competence_id INT,
    type_id INT,
    FOREIGN KEY (competence_id) REFERENCES Competence(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (type_id) REFERENCES Type(id) ON DELETE CASCADE ON UPDATE CASCADE
)

