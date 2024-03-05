import os
import json
import time
from pathlib import Path


class GestionnaireListeDachat:
	NOM_FICHIER = "course.json"
	REP_COURANT = Path(__file__).parent / NOM_FICHIER
	OPTIONS_MENU = [
		"1 - Ajouter un élément à la liste d'achat",
		"2 - Retirer un élément de la liste d'achat",
		"3 - Afficher les éléments de la liste d'achat",
		"4 - Vider la liste d'achat",
		"5 - Quitter le programme",
		]
	
	def __init__ (self):
		self.liste = self.charger_liste()
	
	def charger_liste (self):
		if not self.REP_COURANT.exists():
			print("Création de la liste ..")
			time.sleep(3)
			self._ecrire_dans_fichier([])
		else:
			print("Chargement de la liste d'achats...Veuillez patienter")
			time.sleep(2)
		return self._lire_du_fichier()
	
	def _lire_du_fichier (self):
		with self.REP_COURANT.open("r") as f:
			return json.load(f)
	
	def _ecrire_dans_fichier (self, donnees):
		with self.REP_COURANT.open("w") as f:
			json.dump(donnees, f, indent = 4)
	
	def ajouter_article (self):
		article = input("Que voulez-vous ajouter à la liste ? ")
		self.liste.append(article)
		self._ecrire_dans_fichier(self.liste)
		print("Ajout réussi !")
	
	def supprimer_article (self):
		article = input("Que voulez-vous supprimer de la liste ? ")
		try:
			self.liste.remove(article)
			self._ecrire_dans_fichier(self.liste)
			print("Article supprimé avec succès !")
		except ValueError:
			print("ERREUR -- Veuillez vérifier la saisie de l'article à supprimer !")
			time.sleep(3)
	
	def afficher_articles (self):
		print("Actuellement dans la liste -->")
		time.sleep(2)
		print(self.liste)
	
	def vider_liste (self):
		confirmer = input("Confirmer la suppression de la liste ? Y/N ")
		if confirmer.lower() == "y":
			self.liste = []
			self._ecrire_dans_fichier(self.liste)
			print("Liste vidée !")
			time.sleep(3)
	
	def quitter_programme (self):
		confirmer = input("Voulez-vous vraiment quitter ? Y/N ")
		if confirmer.lower() == "y":
			print("Au revoir !")
			time.sleep(4)
			exit()
	
	def executer (self):
		while True:
			print("Bienvenu sur l'utilitaire, veuillez choisir parmi les options suivantes :")
			print(*self.OPTIONS_MENU, sep = '\n')
			choix_utilisateur = input("Entrez le numéro de votre sélection : ")
			if choix_utilisateur.isdigit():
				choix_utilisateur = int(choix_utilisateur)
				if choix_utilisateur == 1:
					self.ajouter_article()
				elif choix_utilisateur == 2:
					self.supprimer_article()
				elif choix_utilisateur == 3:
					self.afficher_articles()
				elif choix_utilisateur == 4:
					self.vider_liste()
				elif choix_utilisateur == 5:
					self.quitter_programme()
				else:
					print("ATTENTION -- Veuillez saisir un des choix du menu !")
					time.sleep(3)


if __name__ == "__main__":
	gestionnaire = GestionnaireListeDachat()
	gestionnaire.executer()
