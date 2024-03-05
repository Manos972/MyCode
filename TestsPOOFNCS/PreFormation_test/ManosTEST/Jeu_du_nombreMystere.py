# Le but de ce projet est de permettre à un joueur d'essayer de deviner un nombre mystère généré aléatoirement par l'ordinateur, en 5 essais ou moins.
# Déroulé du script
# Au début du script, vous devez générer un nombre aléatoire compris entre 0 et 100 (vous pouvez agrandir ou réduire cet intervalle pour simplifier ou complexifier le jeu).
# Le joueur dispose alors de 5 essais (là encore, libre à vous de changer cette valeur) pour trouver le nombre mystère.
# À chaque essai, vous devez indiquer au joueur si le nombre qu'il a entré est plus petit ou plus grand que le nombre mystère.
# Si le nombre entré par l'utilisateur est égal au nombre mystère, alors le joueur gagne la partie.
# Dans le cas d'une victoire, vous devez indiquer au joueur combien d'essais lui ont été nécessaire pour gagner.
# Si le joueur ne trouve pas le nombre mystère avec les 5 essais disponibles, il perd la partie.

import random
import sys
import time

r = random.randint(0, 15)
chance = 0
promte = "Bienvenu sur le jeu du Nombre Mystère ! "
promte_rules = "Vous disposez de 5 essais pour trouver le nombre Mystère :) A vous de jouer ! "
print(promte, promte_rules)

while chance < 5 :
    user_choice = input("Veuillez choisir un chiffre compris entre 0 et 15 : ")
    var_verif = user_choice.isdigit()
    if var_verif == True :
        user_choice = int(user_choice)
        if user_choice < r and chance != 5 :
            print(f"Le nombre Mystère est plus GRAND que {user_choice}")
            chance += 1
        elif user_choice > r and chance != 5 :
            print(f"Le nombre Mystère est plus PETIT que {user_choice}")
            chance += 1
        elif user_choice == r or chance > 4 :
            if chance > 4 :
                print(f"GAME OVER .. Le Nombre Mystère était {r}")
                retry = input("Voulez-vous rejouer ? o/n ")
                if retry == "o" :
                    r = random.randint(0, 15)
                    chance = 0
                else :
                    print("A bientôt pour une nouvelle partie ! :) ")
                    time.sleep(2)
                    sys.exit()
            elif user_choice == r and chance != 5 :
                time.sleep(3)
                print(f"Congratulation ! Après vos {int(chance + 1)} essais, le Nombre Mystère est bien {user_choice}")
                retry = input("Voulez-vous rejouer ? o/n ")
                if retry == "o" :
                    r = random.randint(0, 15)
                    chance = 0
                else :
                    print("A bientôt pour une nouvelle partie ! :) ")
                    time.sleep(2)
                    sys.exit()
    else :
        print("Veuillez saisir un nombre entier uniquement")
        print(r)
        chance = 0
else :
    print(f"GAME OVER .. Vous avez épuiser tous vos tentatives .. Le Nombre Mystère était {r}")
