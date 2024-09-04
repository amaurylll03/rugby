-- Création de la table Championnat si elle n'existe pas
CREATE TABLE IF NOT EXISTS championnat (
  ID_Championnat INTEGER PRIMARY KEY,
  Nom TEXT NOT NULL,
  Nb_Equipe INTEGER NOT NULL,
  SalaryCap REAL NOT NULL,
  logo_championnat TEXT
);

-- Création de la table Equipe si elle n'existe pas
CREATE TABLE IF NOT EXISTS equipe (
  ID_Equipe INTEGER PRIMARY KEY,
  Nom TEXT NOT NULL,
  Pays TEXT NOT NULL,
  ID_Championnat INTEGER,
  Img_Ecusson TEXT,
  Couleur1 TEXT,
  Couleur2 TEXT,
  budget_equipe INTEGER,
  FOREIGN KEY (ID_Championnat) REFERENCES championnat(ID_Championnat)
);
CREATE TABLE IF NOT EXISTS entraineur (
  ID_Entraineur INTEGER PRIMARY KEY,
  prenom TEXT,
  nom TEXT,
  image TEXT,
  ID_Equipe INTEGER,
  nationalite TEXT,
  nom_carriere TEXT,
  FOREIGN KEY (ID_Equipe) REFERENCES equipe(ID_Equipe)
);

-- Création de la table Joueurs si elle n'existe pas
CREATE TABLE IF NOT EXISTS joueurs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prenom TEXT NOT NULL,
  nom TEXT NOT NULL,
  image TEXT,
  poste INTEGER,
  age INTEGER NOT NULL,
  salaire INTEGER,
  potentiel INTEGER,
  liste_transfert INTEGER,
  valeur INTEGER,
  blessure INTEGER,
  contrat INTEGER,
  titulaire INTEGER,
  ID_Equipe INTEGER,
  FOREIGN KEY (ID_Equipe) REFERENCES equipe(ID_Equipe)
);

-- Création de la table NotesJoueur si elle n'existe pas
CREATE TABLE IF NOT EXISTS notesjoueur (
  id_notes_joueurs INTEGER PRIMARY KEY AUTOINCREMENT,
  id_joueur INTEGER,
  debut_saison INTEGER,
  attaque INTEGER,
  defense INTEGER,
  ruck INTEGER,
  penalite INTEGER,
  melee INTEGER,
  touche INTEGER,
  FOREIGN KEY (id_joueur) REFERENCES joueurs(id)
);

-- Création de la table StatistiquesJoueur si elle n'existe pas
CREATE TABLE IF NOT EXISTS statistiquesjoueur (
  id_statjoueur INTEGER PRIMARY KEY AUTOINCREMENT,
  id_joueur INTEGER,
  essais INTEGER,
  penalite_tente INTEGER,
  penalite_transformee INTEGER,
  nombre_matchs_joue INTEGER,
  FOREIGN KEY (id_joueur) REFERENCES joueurs(id)
);

CREATE TABLE IF NOT EXISTS stade (
  id_stade INTEGER PRIMARY KEY AUTOINCREMENT,
  nom_stade TEXT,
  ID_Equipe INTEGER,
  cpacite_stade INTEGER,
  nombre_tribune INTEGER,
  FOREIGN KEY (ID_Equipe) REFERENCES equipe(ID_Equipe)
);


CREATE TABLE IF NOT EXISTS carriere_en_cours (
  ID_entraineur,
  FOREIGN KEY (ID_entraineur) REFERENCES entraineur(ID_Entraineur)
);
CREATE TABLE IF NOT EXISTS date_du_jour(
  id_date_du_jour INTEGER PRIMARY KEY AUTOINCREMENT,
  jour INTEGER,
  mois INTEGER,
  année INTEGER
);
CREATE TABLE IF NOT EXISTS match(
  id_match INTEGER PRIMARY KEY AUTOINCREMENT,
  id_equipe1 INTEGER,
  id_equipe2 INTEGER,
  id_score1 INTEGER,
  id_score2 INTEGER,
  jour INTEGER,
  mois INTEGER,
  annee INTEGER,
  fin INTEGER

);