from typing import Literal

# Dictionnaire qui stocke les cogs chargés
loaded_ext = list()

online_message = "Salut mon pote !"
ver_num = "2.1.2"

# Fonction pour obtenir les modules chargés
def get_modules() -> list():
    l = list()
    for filename in loaded_ext:
        l.append(filename)
    return l

def add_module(name):
    loaded_ext.append(name)
    
def remove_module(name):
    loaded_ext.remove(name)

# Liste des valeurs pour les commandes
values = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]