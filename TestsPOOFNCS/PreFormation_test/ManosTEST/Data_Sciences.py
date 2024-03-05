# Ouvrir le fichier prenoms.txt et lire son contenu.
#
# Récupérer chaque prénom séparément dans une liste.
#
# Nettoyer les prénoms pour enlever les virgules, points ou espace.
#
# Écrire la liste ordonnée et nettoyée dans un nouveau fichier texte.

import time
from pathlib import Path
prenoms = []
CUR_DIR = Path.home() / "PycharmProjects\TestsPOOFNCS\DossierTest\prenoms.txt"
time.sleep(2)

with open(CUR_DIR, "r", encoding='utf-8', errors = 'ignore') as f :
    opened_file = f.read().splitlines()
# opened_file_clean = opened_file.strip("\n., ")
for p in opened_file:
    prenoms.extend(p.split())
prenoms_clean = [prenom.strip(",. \n") for prenom in prenoms ]

with open(CUR_DIR, "w") as f:
    f.write("\n".join(sorted(prenoms_clean)))
