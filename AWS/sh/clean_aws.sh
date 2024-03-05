#!/bin/bash

# Arrêter et terminer toutes les instances EC2
aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running`].InstanceId' --output text | while read -r instance_id
do
  echo "Arrêt de l'instance $instance_id"
  aws ec2 stop-instances --instance-ids $instance_id
done

aws ec2 wait instance-stopped --instance-ids $(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`stopping`].InstanceId' --output text)

aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`stopped`].InstanceId' --output text | while read -r instance_id
do
  echo "Terminaison de l'instance $instance_id"
  aws ec2 terminate-instances --instance-ids $instance_id
done

# Supprimer les volumes EBS non attachés
aws ec2 describe-volumes --query 'Volumes[?not_null(Attachments[0].InstanceId)] | [?State==`available`].VolumeId' --output text | while read -r volume_id
do
  echo "Suppression du volume EBS non attaché $volume_id"
  aws ec2 delete-volume --volume-id $volume_id
done

echo "Toutes les instances EC2 ont été arrêtées et terminées, et les volumes EBS non attachés ont été supprimés."
