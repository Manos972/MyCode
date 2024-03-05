# Projet liste de courses en POO
import json
import logging
import os

import constants

LOGGER = logging.getLogger()


class Liste(list):
    def __init__(self, nom: str):
        """

        Args:
            nom (object):
        """
        super().__init__()
        self.nom = nom

    def ajouter(self, element):
        """

        Returns:
            object:
        """
        if not isinstance(element, str):
            raise ValueError("Vous ne pouvez ajouter que des châines de caractères !")
        if element in self:
            LOGGER.error(f"{element} est déjà dans la liste.")
            return False
        self.append(element)
        return constants.success_add

    def enlever(self, element: object) -> object:
        """

        Returns:
            object:
        """
        if element in self:
            self.remove(element)
            return constants.success_rem
        LOGGER.error(f"{element} n'est pas dans la liste !")
        return False

    def afficher(self):
        print(f"{constants.info_list} {self.nom}")
        for element in self:
            print(f"- {element}")

    def sauvegarder(self):
        chemin = os.path.join(constants.DATA_DIR, f"{self.nom}.json")

        if not os.path.exists(constants.DATA_DIR):
            os.makedirs(constants.DATA_DIR)

        with open(chemin, "w") as f:
            json.dump(self, f, indent=4)
        return constants.saved


if __name__ == "__main__":
    liste = Liste("Manos")
    result = liste.ajouter(0)
    liste.afficher()
    liste.sauvegarder()
