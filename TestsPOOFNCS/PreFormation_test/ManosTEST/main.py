# This is a sample Python script for testing command and scripts

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Module pour generer un nombre aleatoire
import random

# Module pour interferer avec un systeme d'exploitation (Creer,supp, etc ...)
import os
# chemin = r'C:\Users\Manos\PycharmProjects\pythonProject'
# chemin = os.makedirs("ManosTEST")

# Importe une fonction callable(appelable)
from pprint import pprint

# Verifier que quelquechose est callable
# print(callable(pprint()))


# r = random.randint(0, 1)
# print(r)

# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
# print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm Bitch')


# liste = ["Maxime", "Martine", "Christopher", "Carlos", "Michael", "Eric"]
# print(liste[3:6])


# Gestion des listes

# liste = [1, 2, 3, 4, 5]
# liste.append(6)
# if 6 in liste:
#     print(liste)

# langages = [["Python", "C++"], "Java"]
# nombres = [1, [4, [2, 3]], 5, [6], [[7]]]

# python =  langages[0][0]# entrez le code ici
# deux =  nombres[1][1][0]# entrez le code ici
# sept =  nombres[-1][-1][0]# entrez le code ici
# print(python)
# print(deux)
# print(sept)

# Vérificateur de mot de passe conditionnel
# mdp = input("Entrez un mot de passe (min 8 caractères) : ")
# mdp_trop_court = "votre mot de passe est trop court."
# if len(mdp) == 0 :
#     print(mdp_trop_court.upper())
# elif len(mdp) < 8 :
#     print(mdp_trop_court.capitalize())
# elif mdp.isdigit() :
#     print("Votre mot de passe ne contient que des nombres.")
# else:print("Inscription terminée.")

# Votre script doit afficher les chaînes de caractères suivantes :

# Utilisateur 1
# Utilisateur 2
# Utilisateur 3
# Utilisateur 4
# Utilisateur 5
# Utilisateur 6
# Utilisateur 7
# Utilisateur 8
# Utilisateur 9
# Utilisateur 10
# Votre script doit bien commencer à l'utilisateur 1 et non 0 !

# i=0
# while i in range(1,11):
#     print("Utilisateur"+str(i))
#     i+=1


# Dans cet exercice, vous allez devoir afficher les lettres d'un mot dans l'ordre inverse, lettre par lettre, grâce à une boucle.

# mot = "Python"
# for i in reversed(mot):
#     print(i)
#


# i = 0
# while i < 10:
#     pass
#     i += 1
#     print(i)
# resultat = "Exercice réussi !"

# Comment peut-on permettre à l'utilisateur de sortir de la boucle en modifiant les lignes de code dans la boucle while ?

# continuer = "o"
# while continuer == "o":
#     print("On continue !")
#     continuer = input("Voulez-vous continuer ? o/n ")
# else:print("C'est vous qui voyez, on s'arrête là !")

# num =  random.sample(range(1,100), 10)
# print(num)
# num_impaire = [n for n in num if n % 2 == 1]
# print(num_impaire)


# with open("fichier_txt", "r", encoding='utf-8') as f:
#     contenu = f.read()

# films = {
#     "Le Seigneur des Anneaux" : "12",
#     "Harry Potter" : "9",
#     "Blade Runner" : "7.5",
# }
# prix = 0
#
# for value in films.values():
#     prix += float(value)
#
# print(prix)


employes = {
	"id01" : {"prenom" : "Paul", "nom" : "Dupont", "age" : 32},
	"id02" : {"prenom" : "Julie", "nom" : "Dupuit", "age" : 25},
	"id03" : {"prenom" : "Patrick", "nom" : "Ferrand", "age" : 36}
}

for key, value in employes.items() :
	if value['prenom'] == 'Julie' :
		employes[key]['age'] = 26
	if value['prenom'] == 'Paul' :
		age_paul = employes[key]['age']
print(employes)
print(age_paul)