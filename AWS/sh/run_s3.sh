#!/bin/bash

# Variables
BUCKET_NAME="osmantestgfdsjfgd"   # Remplacez par le nom de votre bucket
FILE_TO_UPLOAD="C:\Users\Manos\PycharmProjects\AWS\run_instance.sh"  # Remplacez par le chemin de votre fichier

# Créer le bucket S3 avec une politique de refus des opérations non chiffrées
aws s3api create-bucket --bucket $BUCKET_NAME --create-bucket-configuration LocationConstraint=eu-west-3

#bucket_policy='{
#  "Version": "2012-10-17",
#  "Statement": [
#    {
#      "Sid": "RequireEncryptedPutObject",
#      "Effect": "Deny",
#      "Principal": "*",
#      "Action": "s3:PutObject",
#      "Resource": "arn:aws:s3:::'$BUCKET_NAME'/*",
#      "Condition": {
#        "StringNotEquals": {
#          "s3:x-amz-server-side-encryption": "AES256"
#        }
#      }
#    }
#  ]
#}'
#echo $bucket_policy > bucket_policy.json
#aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket_policy.json

# Téléverser le fichier dans le bucket

aws s3 cp $FILE_TO_UPLOAD s3://$BUCKET_NAME/

# Lister les objets dans le bucket
aws s3 ls s3://$BUCKET_NAME/
 read -p "Souhaitez-vous maintenant détacher et supprimer le Bucket : o/n " choix
 if [ "$choix" = "o" ]; then
# Supprimer le fichier téléversé
aws s3 rm s3://$BUCKET_NAME/$(basename $FILE_TO_UPLOAD)

# Supprimer le bucket
aws s3 rb s3://$BUCKET_NAME --force

echo "Le fichier et le bucket S3 ont été créés, listés, puis supprimés."
 fi
