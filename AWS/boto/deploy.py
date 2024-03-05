import logging
import csv
from os import system,mkdir
from os.path import exists,splitext
from shutil import chown
from pprint import pprint
from _utils._deploy_utils import user_exists,group_exists

# Initialisation du Fichier/Niveau de logging
logging.basicConfig(filename = "_utils/app_sys.log", filemode = "a", level = logging.INFO, format = "%(asctime)s - %(levelname)s --> %(message)s")


def read_csv (file_to_open):
	"""
	Fonction qui permet de lire le ficier CSV
	:param file: fichier .csv
	:return:list
	"""
	# Tableau qui recevra les données du csv sous forme de list
	tab_csv = []
	
	#Récupère l'extension du fichier
	ext = splitext(file_to_open)
	#On vérifie que l'extension est confome
	if ext[1] != ".csv":
		print("L'extension du fichier chargé n'est pas conforme ! Seuls les .csv sont acceptés")
		logging.error("L'extension du fichier chargé n'est pas conforme ! Seuls les .csv sont acceptés")
	else:
		try:
			# Ouverture et lecture du fichier CSV avec la methode reader du module csv
			with open(file_to_open, "r") as ff:
				csv_content = csv.reader(ff)
				for ligne in csv_content:
					# "Vérifie que la ligne n'est pas vide au quel cas on ne l'intègre pas dans la list"
					if ligne != []:
						tab_csv.append(ligne)
				# Supprime du tableau la 1 ère ligne du CSV qui contient les données non utiles (Nom des colonnes)
				tab_csv.pop(0)
				logging.debug(f"[SYSTEM] - Le fichier .csv --> {file_to_open} à été ouvert et une liste à été créée à partir du CSV ")
				return tab_csv
		except FileNotFoundError:
			print(f"Le fichier .csv saisie --> {file_to_open} n'existe pas")
			logging.error(f"[SYSTEM] - Le fichier .csv --> {file_to_open} n'existe pas ")
			return []

def create_user ():
	"""
	Fonction qui permet de créer les utilisateurs à partir de la sortie de la fonction read_csv
	:return:
	"""
	input_file_user = str(input("Entrer le nom du fichier utilisateurs (.csv) ou chemin absolue : "))
	users_list = read_csv(input_file_user)
	
	for user in users_list:
		# génération du nom utilisateur : on concatène la première lettre du prénom avec le nom
		prenom = user[1]
		nom = user[0]
		user_name = (prenom[0] + nom).lower()
		# On crée l'utilisateur s'il n'existe pas
		if not user_exists(user_name):
			# fonction useradd pour l'ajout de l'utilsateur dans le systeme
			system(f"useradd {user_name}")
			print(f"L'utilisateur --> {user_name} a été créé avec succès.")
			logging.info(f"[INFO] - L'utilisateur --> {user_name} a été créé avec succès.")
		# il n'existe pas :
		else:
			# on récupère le dernier caractère
			indice = user_name[len(user_name) - 1:len(user_name)]
			# print(f"on récupère l'indice du dernier : {indice}")
			# s'il est un numérique, on le caste en numérique
			if (isinstance(indice, int)):
				indice = int(indice)
			else:
				# ce n'est pas un numérique : on prends l'entier 0
				indice = 0
			while (user_exists(user_name + str(indice))):
				# tant que l'utilisateur existe on incrémente de un l'indice qui suivra son nom d'utilisateur
				indice += 1
			# on fabrique le nom avec l'indice
			user_name = user_name + str(indice)
			# fonction useradd pour l'ajout de l'utilsateur dans le systeme
			system(f"useradd {user_name}")
			print(f"L'utilisateur --> {user_name} a été créé avec succès.")
			logging.info(f"[INFO] - L'utilisateur --> {user_name} a été créé avec succès.")

def create_group ():
	"""
	Fonction qui permet de créer les groupes à partir de la sortie de la fonction read_csv
	:return:
	"""
	# on récupère le nom du fichier vie l'entrée utilisateur pour l'envoyer dans la fonction read_csv
	input_file_user = str(input("Entrer le nom du fichier contenant les groupes (.csv) ou chemin absolue  : "))
	group_list = read_csv(input_file_user)
	# Itération pour effectuer les contrôle de champs et les commandes de création de groupes
	for group in group_list:
		groupe = group[1]
		# On utilise la fonction de contôle d'existance du groupe dans le systeme
		if group_exists(groupe):
			print(f"Le groupe '{groupe}' existe déjà.")
			logging.info(f"[INFO] - Le groupe  --> {groupe} existe déjà.")
		
		# On vérifie que le champs "group" n'est pas vide auquel cas on prompte un message à l'utilisateur sur la gestion du systeme pour le groupe
		elif groupe == "":
			print(f"Le groupe '{groupe}' est vide, le systeme laisse la valeur par défaut pour ce dossier.")
			logging.info(f"[INFO] - Le groupe  --> {groupe} est vide, le systeme laisse la valeur par défaut pour ce dossier.")
		
		else:
			try:
				# Créer le groupe si le groupe n'existe pas avec la commande groupadd
				system(f"groupadd {groupe}")
				print(f"Le groupe '{groupe}' a été créé avec succès.")
				logging.info(f"[INFO] - Le groupe  --> {groupe} a été créé avec succès.")
			except Exception as e:
				print(f"Erreur soulevée : {e}")
				logging.error(f"[ERROR] - Une erreure à été soulevée --> {e}.")

def folder_dispatch ():
	"""
	Fonction qui va appliquer à partir du fichier CSV les permissions correspondants aux dossiers,
	Si un dossier n'existe pas il sera créé
	:return:
	"""
	input_file_user = str(input("Entrer le nom du fichier contenant Dossier/permission (.csv) ou chemin absolue : "))
	list_directory = read_csv(input_file_user)
	for element in list_directory:
		# On vérifie si le dossier existe, si non alors on le créé
		if not exists(element[0]):
			# Fonction mkdir pour la creation de Dossier dans le systeme
			mkdir(element[0])
			
			print(f"Le Dossier'{element[0]}' a été créé avec succès.")
			logging.info(f"[INFO] - Le Dossier'{element[0]}' a été créé avec succès.")
		else:
			# On vérifie que la colonne GROUP qui provient du fichier CSV n'est pas vide
			if element[1] != "":
				# On utilise la commande CHOWN du module SHUTIL pour changer le propiétaire du dossier
				chown(element[0], group = element[1])
				
				print(f"Le propiétaire de '{element[0]}' a été mis à jour avec succès.")
				logging.info(f"[INFO] - Le propiétaire de '{element[0]}' a été mis à jour avec succès.")
			# Enfin on modifie/crée les permissions associées au dossier avec la colonne PERMISSIONS du fichier CSV
			system(f"chmod {element[2]} {element[0]}")
			
			print(f"Les permissions de '{element[0]}' ont été mis à jour avec succès.")
			logging.info(f"[INFO] - Les permissions de '{element[0]}' ont été mis à jour avec succès.")

def Deploiement ():
	"""
	Fonction qui va gérer le menu interactif et faire l'appel des fonctions
	:return:
	"""
	while True:
		print("Menu de déploiement.\n")
		print("Veuillez choisir un élément du menu.\n")
		print("1 - Créer les utilisateurs")
		print("2 - Créer les groupes")
		print("3 - Deployer les fichiers et leurs permissions")
		print("4 - Quitter")
		try:
			menu = int(input("Choissisez une option : "))
		except ValueError:
			print("Veuillez saisir un nombre entier en tant qu'option")
		else:
			match menu:
				case 1:
					create_user()
				case 2:
					create_group()
				case 3:
					folder_dispatch()
				case 4:
					print("Sortie... Au revoir.")
					exit()
				case _:
					pprint("Veuillez selectionner une option disponible")


if __name__ == '__main__':
	# print("")
	Deploiement()  # read_csv(file)  # create_user()  # create_group()  # folder_dispatch()
