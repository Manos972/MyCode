import sys
import time
import os
from os.path import exists, isfile
from pprint import pprint

march_arret = True
# liste = []
prompt = "Bienvenu sur l'utilitaire, veuillez choisir parmis les options suivantes : "
prompte_menu = [
    "1 - Ajouter un élément à la liste de courses",
    "2 - Retirer un élément de la liste de courses",
    "3 - Afficher les éléments de la liste de courses",
    "4 - Vider la liste de courses",
    "5 - Quitter le programme",
]
add = "---> Que voulez-vous ajouter à la liste ? "
rem = "---> Que voulez-vous supprimer de la liste ? "
success_add = "------>Ajout réussi !"
success_rem = "------> Suppression réussie !"
cannot_rem = ""
info_list = "Actuellement dans votre liste -->"
empty_list = " !!! La liste actuelle est vide !!! "
confirm_supp_list = "---> Comfirmer la suppression de la liste ? o/n "
cancel_supp_list = "------> Suppression de la liste annulée !"
success_supp_list = "------> Suppression de la liste réussie !"
bye = "-----------> Au revoir ! "
return_menu = "-----------> Retour au menu principal !"
saved = "-----------> La liste a bien été sauvegarder!"

file_course = "Liste"
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, file_course)
