#!/bin/bash

ID_AMI="ami-00983e8a26e4c9bd9"
TYPE_INSTANCE="t2.micro"
NOM_CLE="Osman"
ID_SUBNET="subnet-075b23f367ca55ed1"
read -p "Entrez un nom pour l'instance EC2 : " NOM_INSTANCE

aws ec2 run-instances --image-id "$ID_AMI" --instance-type "$TYPE_INSTANCE" --key-name "$NOM_CLE" --subnet-id "$ID_SUBNET" --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NOM_INSTANCE}]" --output table

sleep 30

aws ec2 describe-instances --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`].Value|[0],InstanceId,InstanceType,State.Name,PublicIpAddress]' --output table
