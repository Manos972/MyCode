# Projet liste de courses

import sys
import time
import os
import json
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
info_list = "Actuellement dans la liste -->"
empty_list = " !!! La liste actuelle est vide !!! "
confirm_supp_list = "---> Comfirmer la suppression de la liste ? o/n "
cancel_supp_list = "------> Suppression de la liste annulée !"
success_supp_list = "------> Suppression de la liste réussie !"
bye = "-----------> Au revoir ! "
return_menu = "-----------> Retour au menu principal !"

file_course = "course.json"
CUR_DIR = os.path.dirname(__file__) + file_course
file_exist = isfile(CUR_DIR)
if not file_exist:
    print("Creation de la liste ..")
    time.sleep(3)
    with open(CUR_DIR, "x") as f:
        liste = json.dump(list(), f, indent=4)
else:
    print("Chargement de la liste de course ... Patientez")
    time.sleep(2)
    with open(CUR_DIR, "r") as f:
        liste = json.load(f)
    pass
print(prompt)
while march_arret == True:
    pprint(prompte_menu)
    user_choice = input("Entrez le numero de votre selection : ")
    if user_choice.isdigit() == True:
        user_choice = int(user_choice)
        if user_choice in range(1, 6):
            if user_choice == 1:
                to_append = input(add)
                with open(CUR_DIR, "r") as f:
                    liste_temp = json.load(f)
                liste_temp.append(to_append)
                with open(CUR_DIR, "w") as f:
                    json.dump(liste_temp, f, indent=4)
                print(success_add)
            elif user_choice == 2:
                # if liste:
                to_remove = input(rem)
                try:
                    with open(CUR_DIR, "r") as f:
                        liste_temp = json.load(f)
                    liste_temp.remove(to_remove)
                    with open(CUR_DIR, "w") as f:
                        json.dump(liste_temp, f, indent=4)
                    print(success_rem)
                except ValueError:
                    print(
                        "ERREUR -- Veuillez vérifier la saisie de l'element à supprimer ! (Voir Menu 3 pour consulter la liste) "
                    )
                    time.sleep(3)
                # else:
                #     print(empty_list)
                # time.sleep(3)
            elif user_choice == 3:
                # if liste:
                print(info_list)
                time.sleep(2)
                with open(CUR_DIR, "r") as f:
                    liste = json.load(f)
                pprint(liste)
                # else:
                # print(empty_list)
                # time.sleep(3)
            elif user_choice == 4:
                supp_ = input(confirm_supp_list)
                if supp_ == "o":
                    with open(CUR_DIR, "w") as f:
                        json.dump(list(), f, indent=4)
                    print(success_supp_list)
                    time.sleep(3)
                else:
                    print(cancel_supp_list)
                    time.sleep(3)
                    march_arret = True
            else:
                exit_ = input("---> Voulez-vous vraiment quitter ? o/n ")
                if exit_ == "o":
                    with open(CUR_DIR, "w") as f:
                        json.dump(liste, f, indent=4)
                    print(bye)
                    time.sleep(4)
                    sys.exit()
                else:
                    print(return_menu)
                    time.sleep(4)
            march_arret = True
        else:
            print("ATTENTION -- Veuillez saisir l'un des choix du menu !")
            time.sleep(3)
            march_arret = True
