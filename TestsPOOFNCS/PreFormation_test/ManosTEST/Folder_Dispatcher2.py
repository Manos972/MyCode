from pathlib import Path

chemin = Path.home() / "TestsPOOFNCS\PreFormation_test\ManosTEST\Dossiertest"

d = {"Films" : ["Le seigneur des anneaux",
                "Harry Potter",
                "Moon",
                "Forrest Gump"],
     "Employes" : ["Paul",
                   "Pierre",
                   "Marie",
                   "Manos"],
     "Exercices" : ["les_variables",
                    "les_fichiers",
                    "les_boucles"]}
for dir in d :
	output = chemin / dir
	output.mkdir(parents = True, exist_ok=True)
	for s_dir in d.get(dir) :
		output_under = output / s_dir
		output_under.mkdir(exist_ok=True)
