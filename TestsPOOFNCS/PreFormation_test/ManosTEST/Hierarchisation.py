# Classe parente
class Animal:
	
	def __init__ (self, nom, age):
		self.nom = nom
		self.age = age
	
	def faire_son_cri (self):
		pass


# Classes enfants
class Chien(Animal):
	
	def faire_son_cri (self):
		return "Woof!"


class Chat(Animal):
	
	def faire_son_cri (self):
		return "Meow!"


# Instanciation des objets
mon_chien = Chien("Tom", 3)
mon_chat = Chat("Jerry", 5)

# Appels de méthodes spécifiques à chaque classe
print(mon_chien.nom, "fait", mon_chien.faire_son_cri())
print(mon_chat.nom, "fait", mon_chat.faire_son_cri())
