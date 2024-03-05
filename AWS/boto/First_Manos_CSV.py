from os.path import splitext
from pprint import pprint
import boto3
import botocore
import logging
import json
import csv

# Configuration du module de log pour inscrire au niveau système les réussite (INFO) ou potentielles erreurs (ERROR/DEBUG)
LOG_FILE = "logs.log"
logging.basicConfig(
	filemode="a",
	filename=LOG_FILE,
	level=logging.INFO,
	encoding="UTF-8",
	format="%(asctime)s - %(levelname)s -> %(message)s",
)
logger = logging.getLogger(__name__)
# pprint(logger)
# exit()

# Penser à externaliser ces clés pour eviter de les laisser dans le code ou utiliser ~/.aws/credentials, pour un souci de praticité, je les laisse en dur pour le moment

session = boto3.Session(profile_name='default')

# Client IAM
clientIAM = session.client('iam')

# fichier json pour les logins
file_cred = 'user_cred.json'
file_to_open = "profil.csv"

required_column = ['username', 'password', 'group', 'policy']
prefix = "Manos_"
def read_csv(file_to_open):
    """
    Fonction qui permet de lire le fichier CSV
    :param file_open: fichier .csv
    :return: list
    """
    tab_csv = []
    ext = splitext(file_to_open)
    if ext[1] != ".csv":
        print("L'extension du fichier chargé n'est pas conforme ! Seuls les .csv sont acceptés")
        logging.error("L'extension du fichier chargé n'est pas conforme ! Seuls les .csv sont acceptés")
    else:
        try:
            with open(file_to_open, "r") as ff:
                csv_content = csv.reader(ff)
                column_name = next(csv_content)  # Lire la première ligne comme en-tête
                if column_name == required_column:
                    for ligne in csv_content:
                        if ligne:
                            tab_csv.append(ligne)
                    if tab_csv:
                        tab_csv.pop(0)
                        logging.debug(f"[SYSTEM] - Le fichier .csv --> {file_to_open} a été ouvert et une liste a été créée à partir du CSV ")
                else:
                    print(f"Veuillez vérifier les colonnes du fichier .csv . Instencier vos colonnes comme suit -->  {required_column}.")
                    logging.error(f"Veuillez vérifier les colonnes du fichier .csv . Instencier vos colonnes comme suit -->  {required_column}.")
                return tab_csv
        except FileNotFoundError:
            print(f"Le fichier .csv saisi --> {file_to_open} n'existe pas")
            logging.error(f"[SYSTEM] - Le fichier .csv --> {file_to_open} n'existe pas ")
    return []

tableau = read_csv(file_to_open)

def first():
	'''
	Cette fonction est le point d'entrée principal du script
	'''
	for elmnt in tableau:
		user_name = prefix + elmnt[0]
		user_password = elmnt[1]
		group_name_s3 = prefix + elmnt[2]
		policy_name = elmnt[3]
		group_create(group_name_s3)
		group_policy(group_name_s3, policy_name)
		create_user(user_name,user_password)
		group_add(user_name, group_name_s3)
		access_key = generate_access_key(user_name)
		save(file_cred, user_name, access_key)

def user_exist(user_name):
	'''
	Cette fonction vérifie si un utilisateur donné existe déjà
	Args:
	user_name: str

	Returns: bool
	'''
	try:
		clientIAM.get_user(UserName=user_name)
		logger.debug(f"L'utilisateur {user_name} existe déjà.")
		pprint(f"L'utilisateur {user_name} existe déjà.")
		return True
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == 'NoSuchEntity':
			logger.info(f"L'utilisateur {user_name} a été créé.")
			pprint(f"L'utilisateur {user_name} a été créé.")
			return False
		else:
			raise

def group_exists(group_name):
	'''
	Cette fonction vérifie si un groupe donné existe
	Args:
	group_name: str

	Returns: bool
	'''
	try:
		clientIAM.get_group(GroupName=group_name)
		logger.debug(f"Le groupe {group_name} existe déjà.")
		pprint(f"Le groupe {group_name} existe déjà.")
		return True
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == 'NoSuchEntity':
			logger.info(f"Le groupe {group_name} a été créé.")
			pprint(f"Le groupe {group_name} a été créé.")
			return False
		else:
			raise

def create_user(user_name, user_password):
	'''
	Cette fonction crée un utilisateur
	Args:
	user_name: str

	Returns: None
	'''
	if not user_exist(user_name):
		clientIAM.create_user(UserName=user_name)
		
		clientIAM.create_login_profile(
			UserName=user_name,
			Password=user_password,
			PasswordResetRequired=True|False
			)

def group_create(group_name_s3):
	'''
	Cette fonction crée un groupe
	Args:
	group_name_s3: str

	'''
	if not group_exists(group_name_s3):
		clientIAM.create_group(GroupName=group_name_s3) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM
def group_policy(group_name, policy_name):
	'''
	Cette fonction attribue un politique ARN à un groupe donné
	Args:
		group_name: str
		policy_name: str

	Returns: dict

	'''
	policy_arn = f'{policy_name}'
	clientIAM.attach_group_policy(GroupName=group_name, PolicyArn=str(policy_arn)) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM
def group_add(user_name, group_name):
	'''
	Cette fonction ajoute l'utilisateur passé en paramètre à un groupe donné
	Args:
	user_name: str
	group_name: str

	Returns: dict

	'''
	clientIAM.add_user_to_group(UserName=user_name, GroupName=group_name) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM

def generate_access_key(user_name):
	'''
	Cette fonction crée les clé d'accès utilisateur
	Args:
		user_name: str

	Returns: dict

	'''
	response = clientIAM.create_access_key(UserName=user_name) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM
	pprint(f"Clés d'accès générées pour {user_name}.")
	logger.info(f"Clés d'accès générées pour {user_name}.")
	return response['AccessKey']

def save(file_path, user_name, access_key):
	'''
	Cette fonction sauvegarde les infos dans le json
	Args:
		file_path: fichier de sauvegarde  str
		user_name: nom utilisateur str
		access_key: clé d'accès  str

	Returns:

	'''
	credentials = {
		'User': user_name,
		'AccessKeyId': access_key['AccessKeyId'],
		'SecretAccessKey': access_key['SecretAccessKey']
		}
	with open(file_path, 'w') as file: # On pourrait y mettre le mode a ou w+ pour adapter l'utilisation du json par la suite
		json.dump(credentials, file)
		pprint(f"Les infos utilisateur et AccessKey ont été sauvegardés dans {file_path}.")
		logger.info(f"Les infos utilisateur et AccessKey ont été sauvegardés dans {file_path}.")

if __name__ == '__main__':
	# file_to_open = "profil.csv"
	# tableau = read_csv(file_to_open)
	# for elem in tableau:
	# 	print(f"username {elem[0]}")
	# 	print(f"password {elem[1]}")
	# 	print(f"group {elem[2]}")
	# 	print(f"policy {elem[3]}")
	first()
