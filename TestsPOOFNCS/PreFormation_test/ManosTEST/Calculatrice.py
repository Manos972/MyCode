
# Projet CALCULATRICE

march_arret = True
while march_arret == True:
        n1 = input('Veuillez entrer un premier nombre :')
        n2 = input('Veuillez entrer un deuxième nombre a additionner :')
        if n1.isdigit() and n2.isdigit() == True:
            n_result = f"Le résultat de l'addition de {int(n1)} avec {int(n2)} est égal à {int(n1) + int(n2)}"
            print(n_result)
            march_arret = False
        else:
            print("Veuillez saisir deux nombres entiers !")
            march_arret = True
