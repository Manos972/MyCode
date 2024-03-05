import time
from pathlib import Path
prenoms = []
CUR_DIR = Path.home() / "PycharmProjects\\DossierTest\\Detection.lnk"
time.sleep(2)

try:
	with open(CUR_DIR, "r") as f :
		opened_file = f.read().splitlines()
	# opened_file_clean = opened_file.strip("\n., ")
except SyntaxError:
	print("Une erreur de syntaxe de la condition ")
except FileNotFoundError:
	print("Le fichier rechercher n'existe pas ")
except UnicodeDecodeError:
	print("Impossible d'ouvrir le fichier.")
else:
	for p in opened_file:
		prenoms.extend(p.split())
	prenoms_clean = [prenom.strip(",. \n") for prenom in prenoms ]

	with open(CUR_DIR, "w") as f:
		f.write("\n".join(sorted(prenoms_clean)))