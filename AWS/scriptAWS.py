import boto3
from os import path
import sys

#Vérification du nombre d'argument

arg = sys.argv

if arg != 2:
	print("Veuillez entrer au moins un arguments")
	exit()

directory = arg[1]

if not path.exists(directory):
	print("Le repertoire n'existe pas !")
	exit()

DB = boto3.resource('dynamodb')
# Create the DynamoDB table.
table = DB.create_table(
	TableName='S3FileMetadata',
	KeySchema=[
		{
			'AttributeName': 'FileID',
			'KeyType': 'HASH'
			},
		{
			'AttributeName': 'FileName',
			'KeyType': 'RANGE'
			},
		{
			'AttributeName': 'FileSize',
			'KeyType': 'RANGE'
			},
		{
			'AttributeName': 'LastModified',
			'KeyType': 'RANGE'
			},
		{
			'AttributeName': 'S3Path',
			'KeyType': 'RANGE'
			},
		{
			'AttributeName': 'MD5Hash',
			'KeyType': 'RANGE'
			}
		],
	AttributeDefinitions=[
		{
			'AttributeName': 'FileID',
			'KeyType': 'S'
			},
		{
			'AttributeName': 'FileName',
			'KeyType': 'S'
			},
		{
			'AttributeName': 'FileSize',
			'KeyType': 'N'
			},
		{
			'AttributeName': 'LastModified',
			'KeyType': 'S'
			},
		{
			'AttributeName': 'S3Path',
			'KeyType': 'S'
			},
		{
			'AttributeName': 'MD5Hash',
			'KeyType': 'S'
			}
		
		],
	ProvisionedThroughput={
		'ReadCapacityUnits': 5,
		'WriteCapacityUnits': 5
		}
	)

# Wait until the table exists.
table.wait_until_exists()
# Print out some data about the table.
print(table.item_count)
