from pprint import pprint
import boto3
import botocore
import logging
import json

# Configuration du module de log pour inscrire au niveau système les réussite (INFO) ou potentielles erreurs (ERROR/DEBUG)
LOG_FILE = "logs_2024.log"
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
# PrefixManos pour lisisbilité
prefix = "Manos_"
# Group IAM
group_name_s3 = prefix + 'S3ReadOnlyGroupXYZ'
# User IAM
user_name = prefix + 'CloudSysOpsXYZ'
# fichier json pour les logins
file_cred = 'user_cred.json'

def first():
	'''
	Cette fonction est main et permet le déroulement principal du script
	Returns:

	'''
	try:
		if not group_exists(group_name_s3): # Vérifie si le groupe Manos_S3ReadOnlyGroup existe auquel cas, on le crée et fournit le retour et incrit un log en fonction
			group_create()
			pprint(f"Le groupe {group_name_s3} à été créé.")
			logger.info(f"Le groupe {group_name_s3} à été créé.")
		else:
			pprint(f"Le groupe {group_name_s3} existe déjà.")
			logger.debug(f"Le groupe {group_name_s3} existe déjà.")
		
		group_policy(group_name_s3, 'AmazonS3ReadOnlyAccess') # Fonction group_policy() pour lier AmazonS3ReadOnlyAccess au groupe Manos_S3ReadOnlyGroup
		
		if not user_exist(user_name): # Vérifie si l'utilisateur Manos_CloudSysOps existe auquel cas, on le crée et fournit le retour et incrit un log en fonction
			create_user()
			pprint(f"L'utilisateur {user_name} à été créé.")
			logger.info(f"L'utilisateur {user_name} à été créé.")
		else:
			pprint(f"L'utilisateur {user_name} existe déjà.")
			logger.debug(f"L'utilisateur {user_name} existe déjà.")
		
		groupadd(user_name, group_name_s3) # Ajoute l'utilisateur Manos_CloudSysOps au groupe Manos_S3ReadOnlyGroup
		
		access_key = generate_access_key(user_name) # Crée AccessKey pour l'utilisateur
		pprint(f"Clés d'accès générées pour {user_name}.")
		logger.info(f"Clés d'accès générées pour {user_name}.")
		
		# Save() AccessKey / utilisateur dans le json
		save(file_cred, user_name, access_key)
	except botocore.exceptions.ClientError as e:  # On lève une exception en cas d'erreurs
		logger.error(f"Erreur raise -->  {e}")

def user_exist(user_name):
	'''
	Cette foncction vérifie si un utilisateur donné existe déjà
	Args:
		user_name: str

	Returns: bool | exeception

	'''
	try:
		clientIAM.get_user(UserName=user_name) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM
		return True
	except botocore.exceptions.ClientError as e:
		# pprint(e)
		# exit()
		if e.response['Error']['Code'] == 'NoSuchEntity':  # si on recoit --> 'NoSuchEntity' c'est que l'user n'existe pas
			return False
		else:
			raise

def group_exists(group_name):
	'''
	Cette fonction vérifie si un utilisateur existe
	Args:
		group_name:

	Returns: bool | exeception

	'''
	try:
		clientIAM.get_group(GroupName=group_name) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM
		return True
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == 'NoSuchEntity': # si on recoit --> 'NoSuchEntity' c'est que le groupe n'existe pas
			return False
		else:
			raise

def create_user():
	'''
	Cette fonction créer un utilisateur
	Returns: dict

	'''
	# pprint(type(clientIAM.create_user(UserName=user_name)))
	clientIAM.create_user(UserName=user_name) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM

def group_create():
	'''
	Cette fonction créer un groupe
	Returns: dict

	'''
	clientIAM.create_group(GroupName=group_name_s3) # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM

def group_policy(group_name, policy_name):
	'''
	Cette fonction attribue un politique ARN à un groupe donné
	Args:
		group_name: str
		policy_name: str

	Returns: dict

	'''
	clientIAM.attach_group_policy(GroupName=group_name, PolicyArn=f'arn:aws:iam::aws:policy/{policy_name}') # Appel de la methode sur l'objet IAM instancier plus haut --> clientIAM

def groupadd(user_name, group_name):
	'''
	Cette fonction ajoute l'utilisateur passé en paramètre à un groupe donné
	Args:
		user_name:  str
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
	first()
