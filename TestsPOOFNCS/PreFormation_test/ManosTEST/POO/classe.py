# coding=utf-8
from dataclasses import dataclass


@dataclass
class Car:
    roue = 4

    def __init__(self, marque: object, couleur: object, prix: object) -> object:
        """

        Args:
            couleur (object):
        """
        self.marque = marque
        self.couleur = couleur
        self.prix = prix


# print(Car.marque)
# print(Car.couleur)

voiture_01 = Car("Dacia", "Blue", "200.000")

voiture_02 = Car("Peugeot", "Red", "200.000")

# print(voiture_01.marque)
# print(voiture_02.marque)


class Voiture:
    def __init__(self):
        self.essence: int = 100

    def afficher_reservoir(self):
        print(f"La voiture contient {self.essence} litres d'essence")

    def roule(self, km: int):
        if self.essence <= 0:
            print(f"Vous n'avez plus d'essence, faites le plein ! ")
            return
        self.essence -= (km * 5) / 100
        if self.essence < 10:
            print(f"Vous n'avez bientôt plus d'essence !")
        self.afficher_reservoir()

    def faire_le_plein(self):
        self.essence = 100
        print("Vous pouvez repartir !")
