class CompteBancaire:
	
	def __init__ (self, proprietaire, solde_initial):
		self.proprietaire = proprietaire
		self.__solde = solde_initial  # Encapsulation du solde en tant qu'attribut privé
	
	def deposer (self, montant):
		self.__solde += montant
	
	def retirer (self, montant):
		if montant <= self.__solde:
			self.__solde -= montant
		else:
			print("Solde insuffisant")
	
	def consulter_solde (self):
		return self.__solde


# Création d'un objet compte bancaire
mon_compte = CompteBancaire("My Test", 1000)

# Tentative d'accès direct à l'attribut privé __solde (cela lèvera une erreur)
# print(mon_compte.__solde)

# Déposer de l'argent
mon_compte.deposer(500)

# Retirer de l'argent
mon_compte.retirer(200)

# Consulter le solde
print("Solde actuel:", mon_compte.consulter_solde())
