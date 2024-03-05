import boto3

region = "us-east-1"
vpc_name = "ManosVPC_TP3"
vpc_net = "10.0.0.0/16"
public_subnet = "10.0.4.0/24"
security_group_name = "ManosSecurityGroup_TP3"
key_vpc = "Manos"
instance_type = "t2.micro"
AMI_ID = "ami-0e309a5f3a6dd97ea"
apache_install = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo service httpd start
sudo chkconfig httpd on
"""
# Création du client EC2
Ec2 = boto3.client("ec2", region_name=region)

# Création du VPC
vpc_response = Ec2.create_vpc(CidrBlock=vpc_net)
vpc_id = vpc_response["Vpc"]["VpcId"]
Ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": vpc_name}])
print(f"VPC créé avec l'ID: {vpc_id} et le nom {vpc_name}")

# Attente de la création du VPC
Ec2.get_waiter("vpc_exists").wait(VpcIds=[vpc_id])

# Création de l'Internet Gateway et l'associer au VPC
igw_response = Ec2.create_internet_gateway(
    TagSpecifications=[
        {
            "ResourceType": "internet-gateway",
            "Tags": [
                {"Key": "Name", "Value": "Manos_TP3_IG"},
            ],
        }
    ],
)
igw_id = igw_response["InternetGateway"]["InternetGatewayId"]
Ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
print(f"Internet Gateway créée avec l'ID: {igw_id}")

# Configuration de la table de routage
route_table_response = Ec2.create_route_table(
    VpcId=vpc_id,
    TagSpecifications=[
        {
            "ResourceType": "route-table",
            "Tags": [
                {"Key": "Name", "Value": "Manos_TP3_RouteTAable"},
            ],
        }
    ],
)
route_table_id = route_table_response["RouteTable"]["RouteTableId"]
Ec2.create_route(
    RouteTableId=route_table_id,
    DestinationCidrBlock="0.0.0.0/0",
    GatewayId=igw_id,
)
print(f"Table de routage configurée avec l'ID: {route_table_id}")

# Création du sous-réseau public
subnet_response = Ec2.create_subnet(
    VpcId=vpc_id,
    CidrBlock=public_subnet,
    TagSpecifications=[
        {
            "ResourceType": "subnet",
            "Tags": [
                {"Key": "Name", "Value": "Manos_TP3_PubSubnet"},
            ],
        }
    ],
)
Ec2.modify_subnet_attribute(
    SubnetId=subnet_response["Subnet"]["SubnetId"], MapPublicIpOnLaunch={"Value": True}
)
subnet_id = subnet_response["Subnet"]["SubnetId"]
print(f"Sous-réseau public créé avec l'ID: {subnet_id}")

# Associez la table de routage au sous-réseau
Ec2.associate_route_table(SubnetId=subnet_id, RouteTableId=route_table_id)
print(f"Table de routage associée au sous-réseau avec l'ID: {subnet_id}")

# Création du Security Group
security_group_response = Ec2.create_security_group(
    GroupName=security_group_name,
    Description="Permet SSH et HTTP pour VPC Manos",
    VpcId=vpc_id,
)
security_group_id = security_group_response["GroupId"]
Ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
    ],
)
print(f"Security Group créé avec l'ID: {security_group_id}")

# Lancement de l'instance EC2
instance_response = Ec2.run_instances(
    ImageId=AMI_ID,
    InstanceType=instance_type,
    KeyName=key_vpc,
    MinCount=1,
    MaxCount=1,
    NetworkInterfaces=[
        {
            "SubnetId": subnet_id,
            "Groups": [security_group_id],
            "DeviceIndex": 0,
        }
    ],
    UserData=apache_install,
    TagSpecifications=[
        {
            "ResourceType": "instance",
            "Tags": [
                {"Key": "Name", "Value": "Manos_EC2_TP3"},
            ],
        }
    ],
)
instance_id = instance_response["Instances"][0]["InstanceId"]
print(f"Instance EC2 lancée avec l'ID: {instance_id}")

# Attente de l'initialisation de l'instance
Ec2.get_waiter("instance_status_ok").wait(InstanceIds=[instance_id])

# Obtention de l'adresse IP publique de l'instance
instance_info = Ec2.describe_instances(InstanceIds=[instance_id])["Reservations"][0][
    "Instances"
][0]

if "PublicIpAddress" in instance_info:
    public_ip = instance_info["PublicIpAddress"]
    print(f"Adresse IP publique de l'instance EC2: {public_ip}")
else:
    print("L'instance n'a pas d'adresse IP publique.")
