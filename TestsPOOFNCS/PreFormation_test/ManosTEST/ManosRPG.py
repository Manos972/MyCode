# Règles du jeu
# Le but de ce projet est de créer un jeu de rôle textuel dans le terminal.
# Le jeu comporte deux joueurs : vous et un ennemi.
# Vous commencez tous les deux avec 50 points de vie.
# Votre personnage dispose de 3 potions qui vous permettent de récupérer des points de vie.
# L'ennemi ne dispose d'aucune potion.
# Chaque potion vous permet de récupérer un nombre aléatoire de points de vie, compris entre 15 et 50.
# Votre attaque inflige à l'ennemi des dégâts aléatoires compris entre 5 et 10 points de vie.
# L'attaque de l'ennemi vous inflige des dégâts aléatoires compris entre 5 et 15 points de vie.
# Lorsque vous utilisez une potion, vous passez le prochain tour.
# Déroulé de la partie
# Lorsque vous lancez le script, vous devez demander à l'utilisateur s'il souhaite attaquer ou utiliser une potion :
# "Souhaitez-vous attaquer (1) ou utiliser une potion (2) ? "
# Cette phrase sera demandée à l'utilisateur au début de chaque tour.
# ?  Si l'utilisateur choisi la première option (1), vous infligez des points de dégât à l'ennemi.
# Ces points seront compris entre 5 et 10 et déterminés aléatoirement par le programme.
# ?  Si l'utilisateur choisi la deuxième option (2), vous prenez une potion.
# Les points de vie que la potion vous donne doivent être compris entre 15 et 50 et générés aléatoirement par le programme Python.
# Vous devez vérifier que l'utilisateur dispose de suffisamment de potion et décrémenter le nombre de potions qu'il a dans son inventaire lorsqu'il en boit une. Si l'utilisateur n'a plus de potions, vous devez lui indiquer et lui proposer de nouveau de faire un choix (attaquer ou prendre une potion).
# Quand le joueur prend une potion, il passe le prochain tour.
# Une fois l'action du joueur exécutée, et si l'ennemi est encore vivant, il vous attaque. Si l'ennemi est mort, vous pouvez terminer le jeu et indiqué à l'utilisateur qu'il a gagné ?
# L'attaque de l'ennemi inflige des dégâts au joueur compris entre 5 et 15, là encore déterminés aléatoirement par le script.
# Si vous n'avez plus de points de vie, le jeu se termine et vous avez perdu la partie.
# À la fin du tour, vous devez afficher le nombre de points de vie restants du joueur et de l'ennemi.
# Toutes ces opérations se répètent tant que le joueur et l'ennemi sont en vie.
# À chaque tour, vous attaquez en premier. Il ne peut donc pas y avoir de match nul. Si lorsque vous attaquez, votre attaque fait descendre les points de vie de l'ennemi en dessous (ou égal à) 0, vous gagnez la partie sans que l'ennemi n'ait le temps de vous attaquer en retour.
import random
import time

SANTE_JOUEUR = 50
SANTE_ENNEMI = 50
tour_joueur = True
tour_ennemi = False
compte_potion_joueur = 3
RESTAURATION_SANTE_POTION = random.randint(15, 50)
DEGATS_ATTAQUE_JOUEUR = random.randint(15, 20)
DEGATS_ATTAQUE_ENNEMI = random.randint(20, 25)


def afficher_resultat (msg1, msg2, msg3):
	max_len = max(len(msg1), len(msg2), len(msg3))
	msg1 += ' ' * (max_len - len(msg1))
	msg2 += ' ' * (max_len - len(msg2))
	msg3 += ' ' * (max_len - len(msg3))
	print('+' * (max_len + 4))
	print('+', msg1, '+')
	print('+', msg2, '+')
	print('+', msg3, '+')
	print('+' * (max_len + 4))

while True:
	afficher_resultat('Résultat du combat:',
	                  f'Le joueur a {SANTE_JOUEUR} PV',
	                  f'L\'ennemi a {SANTE_ENNEMI} PV')
	
	if tour_joueur:
		print("Votre tour")
		time.sleep(2)
		while True:
			try:
				action_joueur = int(input("Voulez-vous attaquer (1) ou utiliser une potion (2) ? "))
			except ValueError:
				print("Entrée invalide, veuillez entrer 1 pour attaquer ou 2 pour utiliser une potion.")
			else:
				if action_joueur in [1, 2]:
					break
				else:
					print("Choix invalide, veuillez entrer 1 pour attaquer ou 2 pour utiliser une potion.")
		if action_joueur == 1:
			SANTE_ENNEMI -= DEGATS_ATTAQUE_JOUEUR
			if SANTE_ENNEMI > 0:
				print(f"Vous infligez {DEGATS_ATTAQUE_JOUEUR} de dégâts, il reste {SANTE_ENNEMI} PV à l'ennemi.")
			else:
				print("L'ennemi n'a plus de PV.")
			tour_joueur = False
			tour_ennemi = True
		elif action_joueur == 2:
			if compte_potion_joueur > 0:
				SANTE_JOUEUR += RESTAURATION_SANTE_POTION
				compte_potion_joueur -= 1
				print(f"Vous utilisez une potion et récupérez {RESTAURATION_SANTE_POTION} PV. Vous avez encore"
				      f" {compte_potion_joueur} potion et votre santé totale est de {SANTE_JOUEUR}")
				tour_joueur = False
				tour_ennemi = True
			else:
				print("Plus de potions disponibles, vous passez le tour suivant")
				tour_joueur = False
				tour_ennemi = True
				continue
	elif tour_ennemi:
		print("Tour de l'ennemi")
		time.sleep(2)
		SANTE_JOUEUR -= DEGATS_ATTAQUE_ENNEMI
		if SANTE_JOUEUR > 0:
			print(f"L'ennemi vous inflige {DEGATS_ATTAQUE_ENNEMI} de dégâts, il reste {SANTE_JOUEUR} PV au joueur.")
		else:
			print("Le joueur n'a plus de PV.")
		tour_ennemi = False
		tour_joueur = True
	
	if SANTE_JOUEUR <= 0:
		print("Vous avez perdu la partie")
		break
	elif SANTE_ENNEMI <= 0:
		print("Vous avez gagné la partie")
		break
