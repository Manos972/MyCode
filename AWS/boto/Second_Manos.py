import time
from pprint import pprint

import boto3
import botocore

# Remplacez ces valeurs par les vôtres
bucket = "elmanos972bucket"
AMI_ID = "ami-0e309a5f3a6dd97ea"
key_bucket = "Osman"
ec2_instance_type = "t2.micro"
prefix = "Manos_"
subnet = "subnet-06303f9e17d905903"
# Rôle IAM et politique
role_name = f"{prefix}WebAppS3ReadOnlyRole"
policy_name = "WebAppS3ReadOnlyPolicy"

# Profil d'instance IAM
instance_profile_name = "WebAppInstanceProfile"

# Crée une session Boto3
session = boto3.Session(profile_name="default")

# Crée un client IAM
IAM = session.client("iam")

# Crée un client EC2
Ec2 = session.client("ec2")


# Vérifie si le rôle IAM existe
def role_exists():
    try:
        IAM.get_role(RoleName=role_name)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            IAM.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument="""{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}""",
            )
            s3_bucket_arn = f"arn:aws:s3:::{bucket}/*"
            policy_document = f"""{{"Version": "2012-10-17","Statement": [{{"Effect": "Allow","Action": "s3:GetObject","Resource": "{s3_bucket_arn}"}}]}}"""
            IAM.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=policy_document,
            )
        else:
            raise


# Vérifie si le profil d'instance IAM existe
def instance_profile_exists():
    try:
        IAM.get_instance_profile(InstanceProfileName=instance_profile_name)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchEntity":
            IAM.create_instance_profile(InstanceProfileName=instance_profile_name)
            IAM.add_role_to_instance_profile(
                InstanceProfileName=instance_profile_name, RoleName=role_name
            )
        else:
            raise


print("Création du role...")
role_exists()
print("Role créer avec success")
print("Création du profile d'instance ...")
instance_profile_exists()
print("Profile d'instance créer avec success")

print("Création du Security Group...")
# Création du Security Group
security_group_response = Ec2.create_security_group(
    GroupName="ManosSecurityGroupIAM",
    Description="Permet SSH et HTTP pour instance Manos_IAM",
    VpcId="vpc-008690ff028119f38",
)
# Récupère le Security Group créé
security_group_id = security_group_response["GroupId"]
print(f"Security Group créé avec l'ID : {security_group_id}")

print("Autorisation du trafic SSH dans le Security Group...")
# Autorisation du trafic SSH dans le Security Group
Ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        }
    ],
)
print("Autorisation du trafic SSH terminée.")
print("Lancement d'une nouvelle instance EC2...")
# Lance une nouvelle instance EC2 avec un tag personnalisé et groupe de sécurité personnalisé
response = Ec2.run_instances(
    ImageId=AMI_ID,
    InstanceType=ec2_instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_bucket,
    NetworkInterfaces=[
        {
            "DeviceIndex": 0,
            "AssociatePublicIpAddress": True,
            "Groups": [security_group_id],
            "SubnetId": subnet,
        }
    ],
    IamInstanceProfile={"Name": instance_profile_name},
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": "Manos_IAM_2"},
            ],
        }
    ],
)
# Récupère l'ID de l'instance
instance_id = response["Instances"][0]["InstanceId"]
# Récupère le nom de l'instance
instance_name = response["Instances"][0]["Tags"][0]["Value"]
# Boucle infinie pour vérifier que l'instance est bien en cours d'exécution
while True:
    time.sleep(5)
    instance = Ec2.describe_instances(InstanceIds=[instance_id])["Reservations"][0][
        "Instances"
    ][0]
    state = instance["State"]["Name"]
    if state == "running":
        break
pprint(f"Instance EC2 {instance_id} / {instance_name} est en cours d'exécution.")


def handle_error(error):
    """Affiche un message d'erreur cohérent selon le code d'erreur"""
    error_code = error.response["Error"]["Code"]
    if error_code == "InvalidAMIID.Malformed":
        print(f"Erreur : L'ID de l'image {AMI_ID} est mal formé ou n'existe pas.")
    elif error_code == "InvalidParameterValue":
        print(
            f"Erreur : La valeur du paramètre est invalide, vérifiez les valeurs fournies."
        )
    elif error_code == "NoSuchEntity":
        print(
            f"Erreur : L'entité spécifiée n'existe pas. Vérifiez le groupe, la politique, ou l'utilisateur spécifié."
        )
    elif error_code == "ValidationError":
        print(
            f"Erreur de validation. Assurez-vous que les paramètres requis sont fournis correctement."
        )
    elif error_code == "MissingParameter":
        print(
            f"Erreur : Paramètre manquant. Assurez-vous de fournir tous les paramètres requis."
        )
    elif error_code == "InvalidKeyPair.Duplicate":
        print(f"Erreur : La clé {key_bucket} existe déjà.")
    elif error_code == "VPCIdNotSpecified":
        print(
            f"Erreur : L'ID du VPC n'est pas spécifié. Assurez-vous de fournir l'ID du VPC dans le code."
        )
    elif error_code == "InvalidSubnetID.NotFound":
        print(
            f"Erreur : Le sous-réseau spécifié n'a pas été trouvé. Vérifiez l'ID du sous-réseau."
        )
    elif error_code == "InvalidGroup.NotFound":
        print(
            f"Erreur : Le groupe de sécurité spécifié n'a pas été trouvé. Vérifiez l'ID du groupe de sécurité."
        )
    elif error_code == "UnauthorizedOperation":
        print(
            f"Erreur : Opération non autorisée. Vérifiez les autorisations IAM nécessaires."
        )
    elif error_code == "InvalidGroup.Duplicate":
        print(
            f"Erreur : Le groupe de sécurité {security_group_id} existe déjà pour le VPC choisi"
        )
    else:
        print(
            f"Erreur inattendue : {error.response['Error']['Message']} (Code : {error_code})"
        )
