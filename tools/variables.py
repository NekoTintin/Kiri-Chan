from discord.embeds import Embed

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

subreddit_not_found = Embed(title="<:Erreur:945123023546093611> Subreddit introuvable", description="Le subreddit n'existe pas, vérifie que tu ne t'es pas trompé dans le nom.", color=0xff4300)