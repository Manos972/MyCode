#!/bin/bash

# Variables
TAILLE_VOLUME=12
TYPE_VOLUME="gp2"
ZONE_DISPONIBILITE="eu-west-3c"
ID_INSTANCE="i-08ffbd2ba587bfd81"

# Créer le volume EBS
ID_VOLUME=$(aws ec2 create-volume --size $TAILLE_VOLUME --volume-type $TYPE_VOLUME --availability-zone $ZONE_DISPONIBILITE --query 'VolumID' --output table)

# Attendre que le volume soit disponible
aws ec2 wait volume-available --volume-ids $ID_VOLUME

# Joindre le volume à l'instance EC2
aws ec2 attach-volume --volume-id $ID_VOLUME --instance-id $ID_INSTANCE --device /dev/sdf

# Attendre que le volume soit attaché
aws ec2 wait volume-in-use --volume-ids $ID_VOLUME

read -p "Souhaitez-vous maintenant détacher et supprimer le volume associé a l'instance : o/n " choix
if [ "$choix" = "o" ]; then
  # Détacher le volume de l'instance EC2
  aws ec2 detach-volume --volume-id $ID_VOLUME

  # Attendre que le volume soit détaché
  aws ec2 wait volume-available --volume-ids $ID_VOLUME

  # Supprimer le volume
  aws ec2 delete-volume --volume-id $ID_VOLUME
  echo "Le volume EBS $ID_VOLUME a été créé, attaché, détaché et supprimé."
fi

echo "Le volume EBS $ID_VOLUME a été créé."
